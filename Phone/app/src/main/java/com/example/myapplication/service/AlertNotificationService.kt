package com.example.myapplication.service

import android.app.*
import android.content.Context
import android.content.Intent
import android.content.pm.ServiceInfo
import android.os.Build
import android.os.IBinder
import android.util.Log
import androidx.core.app.NotificationCompat
import com.example.myapplication.MainActivity
import android.media.AudioAttributes
import android.media.AudioManager
import android.media.RingtoneManager
import android.net.Uri
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.collectLatest

class AlertNotificationService : Service() {
    
    private lateinit var alertSoundManager: AlertSoundManager
    private val serviceScope = CoroutineScope(Dispatchers.Default + SupervisorJob())
    
    private val alertSoundUri: Uri by lazy {
        RingtoneManager.getDefaultUri(RingtoneManager.TYPE_ALARM)
            ?: RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION)
            ?: RingtoneManager.getDefaultUri(RingtoneManager.TYPE_RINGTONE)
    }

    companion object {
        private const val FOREGROUND_CHANNEL_ID = "rescue_service_channel"
        private const val ALERT_CHANNEL_ID = "rescue_alerts_channel"
        private const val FOREGROUND_NOTIFICATION_ID = 1
        
        fun start(context: Context, userId: String, token: String) {
            val intent = Intent(context, AlertNotificationService::class.java).apply {
                putExtra("userId", userId)
                putExtra("token", token)
            }
            
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                context.startForegroundService(intent)
            } else {
                context.startService(intent)
            }
        }
        
        fun stop(context: Context) {
            val intent = Intent(context, AlertNotificationService::class.java)
            context.stopService(intent)
        }
    }
    
    override fun onCreate() {
        super.onCreate()
        Log.d("AlertNotificationService", "Service created")
        
        alertSoundManager = AlertSoundManager(this)
        
        createNotificationChannel()
    }
    
    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        Log.d("AlertNotificationService", "Service started")
        
        // Обработка остановки сирены
        if (intent?.action == "STOP_SOUND") {
            Log.d("AlertNotificationService", "Stopping siren")
            alertSoundManager.stopAlertSound()
            return START_STICKY
        }
        
        try {
            val userId = intent?.getStringExtra("userId") ?: return START_NOT_STICKY
            val token = intent.getStringExtra("token") ?: return START_NOT_STICKY
            
            Log.d("AlertNotificationService", "Starting service for user: $userId")
            
            // Запускаем foreground notification
            val notification = createForegroundNotification()
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                startForeground(FOREGROUND_NOTIFICATION_ID, notification, ServiceInfo.FOREGROUND_SERVICE_TYPE_DATA_SYNC)
            } else {
                startForeground(FOREGROUND_NOTIFICATION_ID, notification)
            }
            
            // Подключаемся к WebSocket
            try {
                Log.d("AlertNotificationService", "Connecting to WebSocket...")
                WebSocketManager.connect(userId, token)
                Log.d("AlertNotificationService", "WebSocket connection initiated")
            } catch (e: Exception) {
                Log.e("AlertNotificationService", "WebSocket connection failed", e)
            }
            
            // Слушаем новые вызовы
            serviceScope.launch {
                try {
                    Log.d("AlertNotificationService", "Started listening for new alerts...")
                    WebSocketManager.newAlert.collectLatest { alert ->
                        if (alert != null) {
                            Log.d("AlertNotificationService", "🚨🚨🚨 NEW ALERT RECEIVED!")
                            Log.d("AlertNotificationService", "Alert ID: ${alert.id}")
                            Log.d("AlertNotificationService", "Alert Type: ${alert.type}")
                            Log.d("AlertNotificationService", "Alert Title: ${alert.title}")
                            Log.d("AlertNotificationService", "Alert Status: ${alert.status}")
                            Log.d("AlertNotificationService", "Alert Team ID: ${alert.team_id}")
                            
                            // ВАЖНО: Проигрываем сирену ТОЛЬКО когда вызов назначен команде!
                            // status = "assigned" И team_id != null (оператор назначил команду)
                            val shouldPlaySiren = alert.status == "assigned" && alert.team_id != null
                            
                            if (shouldPlaySiren) {
                                Log.d("AlertNotificationService", "✅ Alert is ASSIGNED to team! Playing siren...")
                                
                                // Проигрываем сирену
                                try {
                                    Log.d("AlertNotificationService", "Playing alert sound...")
                                    alertSoundManager.playAlertSound()
                                    Log.d("AlertNotificationService", "Alert sound started successfully")
                                } catch (e: Exception) {
                                    Log.e("AlertNotificationService", "❌ Failed to play alert sound", e)
                                }
                                
                                // Показываем уведомление
                                try {
                                    Log.d("AlertNotificationService", "Showing notification...")
                                    showAlertNotification(alert.title ?: "Новый вызов", alert.description ?: "")
                                    Log.d("AlertNotificationService", "Notification shown successfully")
                                } catch (e: Exception) {
                                    Log.e("AlertNotificationService", "❌ Failed to show notification", e)
                                }
                                
                                // Автоматически останавливаем сирену через 30 секунд
                                serviceScope.launch {
                                    delay(30000)
                                    Log.d("AlertNotificationService", "Auto-stopping siren after 30 seconds")
                                    alertSoundManager.stopAlertSound()
                                }
                            } else {
                                Log.d("AlertNotificationService", "⏭️ Alert skipped - not assigned to team yet")
                                Log.d("AlertNotificationService", "   Status: ${alert.status}, Team ID: ${alert.team_id}")
                            }
                        } else {
                            Log.d("AlertNotificationService", "Received null alert, skipping...")
                        }
                    }
                } catch (e: Exception) {
                    Log.e("AlertNotificationService", "❌ Error in alert collection", e)
                    e.printStackTrace()
                }
            }
            
            return START_STICKY
        } catch (e: Exception) {
            Log.e("AlertNotificationService", "Service start failed", e)
            return START_NOT_STICKY
        }
    }
    
    override fun onBind(intent: Intent?): IBinder? = null
    
    override fun onDestroy() {
        super.onDestroy()
        Log.d("AlertNotificationService", "Service destroyed")
        
        alertSoundManager.release()
        WebSocketManager.disconnect()
        serviceScope.cancel()
    }
    
    /**
     * Создание канала уведомлений (для Android 8.0+)
     */
    private fun createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val notificationManager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            
            // Канал для фонового сервиса (низкий приоритет)
            val foregroundChannel = NotificationChannel(
                FOREGROUND_CHANNEL_ID,
                "Служба спасения",
                NotificationManager.IMPORTANCE_LOW
            ).apply {
                description = "Фоновая работа службы спасения"
                enableVibration(false)
                enableLights(false)
                setShowBadge(false)
            }
            
            // Канал для экстренных вызовов (высокий приоритет)
            val alertChannel = NotificationChannel(
                ALERT_CHANNEL_ID,
                "Экстренные вызовы",
                NotificationManager.IMPORTANCE_HIGH
            ).apply {
                description = "Критические уведомления о новых экстренных вызовах"
                enableVibration(true)
                enableLights(true)
                setShowBadge(true)
                lockscreenVisibility = Notification.VISIBILITY_PUBLIC
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                    setAllowBubbles(true)
                }
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                    setBypassDnd(true)
                }

                val attributes = AudioAttributes.Builder()
                    .setUsage(AudioAttributes.USAGE_ALARM)
                    .setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION)
                    .build()
                setSound(alertSoundUri, attributes)
            }
            
            notificationManager.createNotificationChannel(foregroundChannel)
            notificationManager.createNotificationChannel(alertChannel)
        }
    }
    
    /**
     * Создание постоянного уведомления для foreground service
     */
    private fun createForegroundNotification(): Notification {
        val intent = Intent(this, MainActivity::class.java)
        val pendingIntent = PendingIntent.getActivity(
            this,
            0,
            intent,
            PendingIntent.FLAG_IMMUTABLE
        )
        
        return NotificationCompat.Builder(this, FOREGROUND_CHANNEL_ID)
            .setContentTitle("Служба спасения")
            .setContentText("Ожидание экстренных вызовов...")
            .setSmallIcon(android.R.drawable.ic_dialog_info)
            .setContentIntent(pendingIntent)
            .setOngoing(true)
            .setSilent(true)
            .setPriority(NotificationCompat.PRIORITY_LOW)
            .build()
    }
    
    /**
     * Показать уведомление о новом вызове
     */
    private fun showAlertNotification(title: String, description: String) {
        Log.d("AlertNotificationService", "📢 showAlertNotification() called")
        Log.d("AlertNotificationService", "Title: $title")
        Log.d("AlertNotificationService", "Description: $description")
        
        val intent = Intent(this, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TOP
        }
        
        val pendingIntent = PendingIntent.getActivity(
            this,
            System.currentTimeMillis().toInt(),
            intent,
            PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT
        )
        
        // Действие для остановки сирены
        val stopSoundIntent = Intent(this, AlertNotificationService::class.java).apply {
            action = "STOP_SOUND"
        }
        val stopSoundPendingIntent = PendingIntent.getService(
            this,
            0,
            stopSoundIntent,
            PendingIntent.FLAG_IMMUTABLE
        )
        
        Log.d("AlertNotificationService", "Building notification...")
        val notification = NotificationCompat.Builder(this, ALERT_CHANNEL_ID)
            .setContentTitle("🚨 ЭКСТРЕННЫЙ ВЫЗОВ!")
            .setContentText(title)
            .setStyle(NotificationCompat.BigTextStyle().bigText(description))
            .setSmallIcon(android.R.drawable.ic_dialog_alert)
            .setContentIntent(pendingIntent)
            .setPriority(NotificationCompat.PRIORITY_MAX)
            .setCategory(NotificationCompat.CATEGORY_ALARM)
            .setAutoCancel(true)
            .setOngoing(false)
            .setVisibility(NotificationCompat.VISIBILITY_PUBLIC)
            .setVibrate(longArrayOf(0, 500, 200, 500, 200, 500))
            .setSound(alertSoundUri, AudioManager.STREAM_ALARM)
            .addAction(
                android.R.drawable.ic_lock_silent_mode_off,
                "Остановить сирену",
                stopSoundPendingIntent
            )
            .setFullScreenIntent(pendingIntent, true)
            .build()
        
        Log.d("AlertNotificationService", "Notification built, showing...")
        val notificationManager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        val notificationId = System.currentTimeMillis().toInt()
        notificationManager.notify(notificationId, notification)
        Log.d("AlertNotificationService", "✅ Notification shown with ID: $notificationId")
    }
}
