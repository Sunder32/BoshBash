package com.example.myapplication.service

import android.util.Log
import com.example.myapplication.data.AppConfig
import com.example.myapplication.data.model.SOSAlert
import com.google.gson.Gson
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import okhttp3.*
import okio.ByteString
import java.util.concurrent.TimeUnit

object WebSocketManager {
    
    private var webSocket: WebSocket? = null
    private val client = OkHttpClient.Builder()
        .readTimeout(30, TimeUnit.SECONDS)
        .writeTimeout(30, TimeUnit.SECONDS)
        .build()
    
    private val wsUrl = AppConfig.websocketUrl
    
    private val _connectionState = MutableStateFlow(ConnectionState.DISCONNECTED)
    val connectionState: StateFlow<ConnectionState> = _connectionState
    
    private val _newAlert = MutableStateFlow<SOSAlert?>(null)
    val newAlert: StateFlow<SOSAlert?> = _newAlert
    
    private var scope: CoroutineScope? = null
    private val gson = Gson()
    
    enum class ConnectionState {
        CONNECTED, DISCONNECTED, CONNECTING, ERROR
    }
    
    /**
     * Подключение к WebSocket серверу
     */
    fun connect(userId: String, token: String) {
        if (webSocket != null) {
            Log.d("WebSocketManager", "Already connected")
            return
        }
        
        // Создаем новый scope при подключении
        scope = CoroutineScope(Dispatchers.IO + SupervisorJob())
        
        _connectionState.value = ConnectionState.CONNECTING
        Log.d("WebSocketManager", "Connecting to: $wsUrl/$userId")
        
        val request = Request.Builder()
            .url("$wsUrl/$userId?token=$token")
            .build()
        
        webSocket = client.newWebSocket(request, object : WebSocketListener() {
            
            override fun onOpen(webSocket: WebSocket, response: Response) {
                Log.d("WebSocketManager", "✅ WebSocket connected successfully!")
                _connectionState.value = ConnectionState.CONNECTED
                
                // Send ping to keep connection alive
                scope?.launch {
                    while (_connectionState.value == ConnectionState.CONNECTED) {
                        webSocket.send("{\"type\":\"ping\"}")
                        delay(30000) // 30 seconds
                    }
                }
            }
            
            override fun onMessage(webSocket: WebSocket, text: String) {
                Log.d("WebSocketManager", "📩 Message received: $text")
                handleMessage(text)
            }
            
            override fun onMessage(webSocket: WebSocket, bytes: ByteString) {
                Log.d("WebSocketManager", "Binary message received")
            }
            
            override fun onClosing(webSocket: WebSocket, code: Int, reason: String) {
                Log.d("WebSocketManager", "WebSocket closing: $code / $reason")
                webSocket.close(1000, null)
                _connectionState.value = ConnectionState.DISCONNECTED
            }
            
            override fun onClosed(webSocket: WebSocket, code: Int, reason: String) {
                Log.d("WebSocketManager", "WebSocket closed: $code / $reason")
                _connectionState.value = ConnectionState.DISCONNECTED
                
                // Попытка переподключения через 5 секунд
                scope?.launch {
                    delay(5000)
                    if (_connectionState.value == ConnectionState.DISCONNECTED) {
                        Log.d("WebSocketManager", "Attempting to reconnect...")
                        connect(userId, token)
                    }
                }
            }
            
            override fun onFailure(webSocket: WebSocket, t: Throwable, response: Response?) {
                Log.e("WebSocketManager", "❌ WebSocket connection failed: ${t.message}", t)
                Log.e("WebSocketManager", "Response: ${response?.message}")
                _connectionState.value = ConnectionState.ERROR
                
                // Попытка переподключения через 10 секунд
                scope?.launch {
                    delay(10000)
                    Log.d("WebSocketManager", "🔄 Attempting to reconnect after failure...")
                    connect(userId, token)
                }
            }
        })
    }
    
    /**
     * Обработка входящего сообщения
     */
    private fun handleMessage(text: String) {
        try {
            Log.d("WebSocketManager", "🔍 Parsing message: $text")
            val message = gson.fromJson(text, WebSocketMessage::class.java)
            
            Log.d("WebSocketManager", "Message type: ${message.type}")
            Log.d("WebSocketManager", "Message data: ${message.data}")
            
            when (message.type) {
                "new_alert" -> {
                    Log.d("WebSocketManager", "🚨🚨🚨 NEW ALERT MESSAGE TYPE DETECTED!")
                    message.data?.let { data ->
                        Log.d("WebSocketManager", "Alert data: $data")
                        val alert = gson.fromJson(gson.toJson(data), SOSAlert::class.java)
                        Log.d("WebSocketManager", "Parsed alert: id=${alert.id}, type=${alert.type}, status=${alert.status}, title=${alert.title}")
                        _newAlert.value = alert
                        Log.d("WebSocketManager", "Alert set to StateFlow, current value: ${_newAlert.value?.id}")
                    } ?: Log.e("WebSocketManager", "❌ Alert data is null!")
                }
                "alert_updated" -> {
                    Log.d("WebSocketManager", "📝 Alert update received")
                    message.data?.let { data ->
                        val alert = gson.fromJson(gson.toJson(data), SOSAlert::class.java)
                        _newAlert.value = alert
                        Log.d("WebSocketManager", "Alert updated: ${alert.id}")
                    }
                }
                "ping" -> {
                    Log.d("WebSocketManager", "🏓 Ping received, sending pong")
                    sendPong()
                }
                "pong" -> {
                    Log.d("WebSocketManager", "🏓 Pong received")
                }
                else -> {
                    Log.d("WebSocketManager", "❓ Unknown message type: ${message.type}")
                }
            }
        } catch (e: Exception) {
            Log.e("WebSocketManager", "❌ Error handling message: ${e.message}", e)
            e.printStackTrace()
        }
    }
    
    /**
     * Отправка pong в ответ на ping
     */
    private fun sendPong() {
        webSocket?.send("""{"type":"pong"}""")
    }
    
    /**
     * Отключение от WebSocket
     */
    fun disconnect() {
        webSocket?.close(1000, "User disconnect")
        webSocket = null
        _connectionState.value = ConnectionState.DISCONNECTED
        scope?.cancel()
        scope = null
    }
    
    /**
     * Отправка сообщения
     */
    fun sendMessage(message: String) {
        webSocket?.send(message)
    }
    
    data class WebSocketMessage(
        val type: String,
        val data: Any? = null
    )
}
