package com.example.myapplication.service

import android.content.Context
import android.media.AudioAttributes
import android.media.AudioFocusRequest
import android.media.AudioManager
import android.media.MediaPlayer
import android.media.RingtoneManager
import android.os.Build
import android.os.VibrationEffect
import android.os.Vibrator
import android.os.VibratorManager
import android.util.Log

class AlertSoundManager(private val context: Context) {
    
    private var mediaPlayer: MediaPlayer? = null
    private var vibrator: Vibrator? = null
    private val audioManager: AudioManager = context.getSystemService(Context.AUDIO_SERVICE) as AudioManager
    private var audioFocusRequest: AudioFocusRequest? = null
    
    init {
        vibrator = if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.S) {
            val vibratorManager = context.getSystemService(Context.VIBRATOR_MANAGER_SERVICE) as VibratorManager
            vibratorManager.defaultVibrator
        } else {
            @Suppress("DEPRECATION")
            context.getSystemService(Context.VIBRATOR_SERVICE) as Vibrator
        }
    }
    
    /**
     * Проигрывает громкий звук сирены при новом вызове
     */
    fun playAlertSound() {
        try {
            Log.d("AlertSoundManager", "🔊 playAlertSound() called")
            
            stopAlertSound() // Останавливаем предыдущий звук если играет
            
            // Используем системный звук уведомления (максимально громкий)
            val alertUri = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_ALARM)
                ?: RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION)
            
            Log.d("AlertSoundManager", "Alert URI: $alertUri")
            
            requestAudioFocus()
            Log.d("AlertSoundManager", "Audio focus requested")

            mediaPlayer = MediaPlayer().apply {
                Log.d("AlertSoundManager", "Setting data source...")
                setDataSource(context, alertUri)
                
                // Настраиваем для максимальной громкости
                setAudioAttributes(
                    AudioAttributes.Builder()
                        .setUsage(AudioAttributes.USAGE_ALARM)
                        .setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION)
                        .build()
                )
                
                // Устанавливаем максимальную громкость
                val currentVolume = audioManager.getStreamVolume(AudioManager.STREAM_ALARM)
                val maxVolume = audioManager.getStreamMaxVolume(AudioManager.STREAM_ALARM)
                Log.d("AlertSoundManager", "Current alarm volume: $currentVolume / $maxVolume")
                audioManager.setStreamVolume(AudioManager.STREAM_ALARM, maxVolume, 0)
                Log.d("AlertSoundManager", "Set alarm volume to max: $maxVolume")
                
                // Зацикливаем звук
                isLooping = true
                Log.d("AlertSoundManager", "Sound set to looping")
                
                setOnPreparedListener {
                    Log.d("AlertSoundManager", "🎵 MediaPlayer prepared, starting playback...")
                    it.start()
                    Log.d("AlertSoundManager", "✅ Alert sound started successfully!")
                }
                
                setOnErrorListener { mp, what, extra ->
                    Log.e("AlertSoundManager", "❌ MediaPlayer error: what=$what, extra=$extra")
                    true
                }
                
                Log.d("AlertSoundManager", "Calling prepareAsync()...")
                prepareAsync()
            }
            
            // Добавляем вибрацию
            Log.d("AlertSoundManager", "Starting vibration...")
            startVibration()
            Log.d("AlertSoundManager", "✅ playAlertSound() completed")
            
        } catch (e: Exception) {
            Log.e("AlertSoundManager", "❌ Error playing alert sound", e)
            e.printStackTrace()
        }
    }
    
    /**
     * Останавливает звук сирены
     */
    fun stopAlertSound() {
        try {
            mediaPlayer?.apply {
                if (isPlaying) {
                    stop()
                }
                release()
            }
            mediaPlayer = null
            
            stopVibration()
            releaseAudioFocus()
            
            Log.d("AlertSoundManager", "Alert sound stopped")
        } catch (e: Exception) {
            Log.e("AlertSoundManager", "Error stopping alert sound", e)
        }
    }

    private fun requestAudioFocus() {
        try {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                val attributes = AudioAttributes.Builder()
                    .setUsage(AudioAttributes.USAGE_ALARM)
                    .setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION)
                    .build()

                audioFocusRequest = AudioFocusRequest.Builder(AudioManager.AUDIOFOCUS_GAIN_TRANSIENT_EXCLUSIVE)
                    .setAudioAttributes(attributes)
                    .setOnAudioFocusChangeListener { }
                    .build()

                audioFocusRequest?.let { audioManager.requestAudioFocus(it) }
            } else {
                @Suppress("DEPRECATION")
                val result = audioManager.requestAudioFocus(
                    null,
                    AudioManager.STREAM_ALARM,
                    AudioManager.AUDIOFOCUS_GAIN_TRANSIENT
                )
                if (result != AudioManager.AUDIOFOCUS_REQUEST_GRANTED) {
                    Log.w("AlertSoundManager", "Audio focus request denied")
                }
            }
        } catch (e: Exception) {
            Log.e("AlertSoundManager", "Error requesting audio focus", e)
        }
    }

    private fun releaseAudioFocus() {
        try {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                audioFocusRequest?.let { request ->
                    audioManager.abandonAudioFocusRequest(request)
                }
                audioFocusRequest = null
            } else {
                @Suppress("DEPRECATION")
                audioManager.abandonAudioFocus(null)
            }
        } catch (e: Exception) {
            Log.e("AlertSoundManager", "Error releasing audio focus", e)
        }
    }
    
    /**
     * Запускает вибрацию по паттерну (сирена)
     */
    private fun startVibration() {
        try {
            if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
                // Паттерн: пауза 0мс, вибрация 500мс, пауза 200мс, повтор
                val timings = longArrayOf(0, 500, 200, 500, 200)
                val amplitudes = intArrayOf(0, 255, 0, 255, 0) // Максимальная амплитуда
                
                val effect = VibrationEffect.createWaveform(timings, amplitudes, 0)
                vibrator?.vibrate(effect)
            } else {
                // Для старых версий Android
                @Suppress("DEPRECATION")
                val pattern = longArrayOf(0, 500, 200, 500, 200)
                @Suppress("DEPRECATION")
                vibrator?.vibrate(pattern, 0)
            }
            
            Log.d("AlertSoundManager", "Vibration started")
        } catch (e: Exception) {
            Log.e("AlertSoundManager", "Error starting vibration", e)
        }
    }
    
    /**
     * Останавливает вибрацию
     */
    private fun stopVibration() {
        try {
            vibrator?.cancel()
            Log.d("AlertSoundManager", "Vibration stopped")
        } catch (e: Exception) {
            Log.e("AlertSoundManager", "Error stopping vibration", e)
        }
    }
    
    /**
     * Проигрывает короткий звук уведомления
     */
    fun playNotificationSound() {
        try {
            val notificationUri = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION)
            val ringtone = RingtoneManager.getRingtone(context, notificationUri)
            ringtone.play()
        } catch (e: Exception) {
            Log.e("AlertSoundManager", "Error playing notification sound", e)
        }
    }
    
    /**
     * Освобождение ресурсов
     */
    fun release() {
        stopAlertSound()
    }
}
