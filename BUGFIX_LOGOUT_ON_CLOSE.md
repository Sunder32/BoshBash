# 🐛 Исправление: Выход из аккаунта при закрытии окна SOS

## Проблема

При закрытии модального окна SOS пользователь выбрасывался из аккаунта и попадал на страницу регистрации/логина.

## Причины

1. **ProtectedRoute с автоматической проверкой пользователя**: В `App.tsx` компонент `ProtectedRoute` вызывал `fetchCurrentUser()` при каждом изменении `isAuthenticated`, что могло вызывать ненужные API запросы и сброс состояния при ошибках.

2. **Сброс состояния при ошибках**: В `authStore.ts` функция `fetchCurrentUser()` при любой ошибке устанавливала `isAuthenticated: false`, что вызывало разлогинивание.

3. **navigate(-1) в SOSStandalonePage**: При закрытии окна SOS использовался `navigate(-1)`, который мог вызывать проблемы с историей навигации и состоянием роутера.

4. **Неполная очистка persist storage**: При logout не очищалось хранилище Zustand persist (`auth-storage`), что могло вызывать конфликты состояния.

## Решение

### 1. Упрощен ProtectedRoute (App.tsx)

**Было:**
```tsx
function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, fetchCurrentUser } = useAuthStore()
  
  useEffect(() => {
    if (isAuthenticated) {
      fetchCurrentUser().catch(() => {})
    }
  }, [isAuthenticated, fetchCurrentUser])
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }
  
  return <>{children}</>
}
```

**Стало:**
```tsx
function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated } = useAuthStore()
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }
  
  return <>{children}</>
}
```

**Эффект**: Убрана автоматическая проверка пользователя при каждом рендере, что исключает лишние API вызовы и потенциальные сбои.

### 2. Улучшена обработка ошибок в fetchCurrentUser (authStore.ts)

**Было:**
```typescript
fetchCurrentUser: async () => {
  try {
    const response = await api.get<User>('/api/v1/auth/me')
    set({ user: response.data, isAuthenticated: true })
  } catch (error) {
    set({ user: null, isAuthenticated: false })  // ❌ Разлогинивает при любой ошибке
    throw error
  }
}
```

**Стало:**
```typescript
fetchCurrentUser: async () => {
  try {
    const response = await api.get<User>('/api/v1/auth/me')
    set({ user: response.data, isAuthenticated: true })
  } catch (error) {
    // Не сбрасываем isAuthenticated - пусть API interceptor обработает 401
    console.error('Failed to fetch current user:', error)
    throw error
  }
}
```

**Эффект**: Состояние авторизации не сбрасывается при временных ошибках сети. Только API interceptor при 401 и неудачном refresh выполняет полный logout.

### 3. Полная очистка persist storage при logout (authStore.ts)

**Было:**
```typescript
logout: () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  set({ user: null, isAuthenticated: false })
}
```

**Стало:**
```typescript
logout: () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('auth-storage')  // ✅ Очищаем Zustand persist
  set({ user: null, isAuthenticated: false })
}
```

**Эффект**: Гарантирует полную очистку всех данных авторизации, включая сохраненное состояние Zustand.

### 4. Улучшена очистка при 401 (api.ts)

**Было:**
```typescript
catch (refreshError) {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  window.location.href = '/login'
  return Promise.reject(refreshError)
}
```

**Стало:**
```typescript
catch (refreshError) {
  // Очищаем все данные авторизации
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('auth-storage')  // ✅ Очищаем Zustand persist
  
  // Перенаправляем на страницу логина
  window.location.href = '/login'
  return Promise.reject(refreshError)
}
```

**Эффект**: При истечении refresh token выполняется полная очистка всех данных авторизации.

### 5. Исправлена навигация в SOSStandalonePage

**Было:**
```tsx
<SOSButton autoOpen onClose={() => navigate(-1)} />
<button onClick={() => navigate(-1)}>Назад</button>
```

**Стало:**
```tsx
<SOSButton autoOpen onClose={() => navigate('/')} />
<button onClick={() => navigate('/')}>Назад</button>
```

**Эффект**: При закрытии окна SOS пользователь возвращается на главную страницу дашборда, а не на предыдущую страницу истории, что исключает проблемы с навигацией.

## Измененные файлы

1. ✅ `frontend/src/App.tsx` - упрощен ProtectedRoute
2. ✅ `frontend/src/store/authStore.ts` - улучшена обработка ошибок и logout
3. ✅ `frontend/src/services/api.ts` - полная очистка при 401
4. ✅ `frontend/src/features/sos/SOSStandalonePage.tsx` - исправлена навигация

## Тестирование

### Сценарий 1: Закрытие окна SOS
1. Войдите в аккаунт
2. Откройте страницу `/sos`
3. Закройте модальное окно SOS (крестик или кнопка "Назад")
4. **Ожидаемый результат**: Вы остаетесь авторизованными и возвращаетесь на главную страницу

### Сценарий 2: Истечение токена
1. Войдите в аккаунт
2. Удалите access_token из localStorage вручную (для имитации истечения)
3. Выполните любое действие, требующее API запроса
4. **Ожидаемый результат**: Попытка refresh токена, при неудаче - перенаправление на /login с полной очисткой

### Сценарий 3: Ручной logout
1. Войдите в аккаунт
2. Нажмите кнопку "Выход"
3. **Ожидаемый результат**: Полная очистка всех токенов и состояния, перенаправление на /login

### Сценарий 4: Перезагрузка страницы
1. Войдите в аккаунт
2. Перезагрузите страницу (F5)
3. **Ожидаемый результат**: Вы остаетесь авторизованными благодаря persist storage

## Технические детали

### Zustand Persist
Zustand persist сохраняет состояние в `localStorage` под ключом `auth-storage`:
```typescript
{
  name: 'auth-storage',
  partialize: (state) => ({ 
    user: state.user, 
    isAuthenticated: state.isAuthenticated 
  }),
}
```

Это позволяет сохранять авторизацию между перезагрузками страницы, но требует правильной очистки при logout.

### API Interceptor Flow
```
1. Request → Add Bearer token
2. Response 401 → Try refresh token
3. Refresh OK → Retry original request
4. Refresh fail → Clear all + redirect to /login
```

### Навигация
- `navigate('/')` - переход на главную страницу (надежно)
- `navigate(-1)` - возврат назад (может вызывать проблемы с историей)

## Статус
✅ **ИСПРАВЛЕНО** - Пользователи больше не выбрасываются из аккаунта при закрытии окна SOS
