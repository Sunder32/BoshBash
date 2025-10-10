import { useCallback, useRef, useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuthStore } from '../../store/authStore'
import { AlertCircle } from 'lucide-react'

interface RegisterForm {
  email: string
  password: string
  full_name: string
  phone: string
}

export default function RegisterPage() {
  const navigate = useNavigate()
  const { register, isLoading, error, clearError } = useAuthStore()
  const formRef = useRef<HTMLFormElement | null>(null)
  
  const [formData, setFormData] = useState<RegisterForm>({
    email: '',
    password: '',
    full_name: '',
    phone: '',
  })

  const handleChange = (field: keyof RegisterForm) => (event: React.ChangeEvent<HTMLInputElement>) => {
    if (error) {
      clearError()
    }
    setFormData((prev) => ({ ...prev, [field]: event.target.value }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    clearError()
    
    try {
      await register({
        ...formData,
        email: formData.email.trim(),
        full_name: formData.full_name.trim(),
        phone: formData.phone.trim(),
      })
      navigate('/')
    } catch (err) {
    }
  }

  const triggerSubmit = useCallback(() => {
    if (isLoading) {
      return
    }
    formRef.current?.requestSubmit()
  }, [isLoading])

  const handleTouchEnd = useCallback((event: React.TouchEvent<HTMLButtonElement>) => {
    event.preventDefault()
    triggerSubmit()
  }, [triggerSubmit])

  const handleKeyUp = useCallback((event: React.KeyboardEvent<HTMLButtonElement>) => {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault()
      triggerSubmit()
    }
  }, [triggerSubmit])

  return (
    <div className="min-h-screen relative flex items-center justify-center px-4 py-12 bg-slate-950 text-slate-100">
      {/* Emergency lights */}
      <div className="emergency-light-red" style={{ top: '10%', left: '10%' }} />
      <div className="emergency-light-blue" style={{ bottom: '10%', right: '10%' }} />

      <div className="relative z-10 w-full max-w-lg">
        <div className="p-8 sm:p-10 backdrop-blur-2xl bg-white/5 rounded-3xl border border-white/20 shadow-2xl">
          <div className="mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-white text-4xl shadow-lg mb-4">
              🚨
            </div>
            <h1 className="text-3xl sm:text-4xl font-semibold text-white drop-shadow-lg">
              Регистрация
            </h1>
            <p className="mt-2 text-sm text-white/90 drop-shadow">
              Создайте аккаунт для доступа к системе
            </p>
          </div>

        {error && (
          <div className="mb-6 bg-rose-50 border border-rose-200 text-rose-700 px-4 py-3 rounded-2xl flex items-center gap-3 animate-fade-in">
            <AlertCircle className="w-5 h-5 flex-shrink-0" />
            <span className="text-sm font-medium">{error}</span>
          </div>
        )}

  <form ref={formRef} onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="register-email" className="block text-sm font-semibold text-white drop-shadow mb-2">
              Email *
            </label>
            <input
              id="register-email"
              type="email"
              required
              autoComplete="email"
              value={formData.email}
              onChange={handleChange('email')}
              className="w-full px-4 py-3 rounded-xl bg-transparent backdrop-blur-md border border-white/30 text-white placeholder:text-white/60 focus:outline-none focus:ring-2 focus:ring-white/50 focus:border-transparent transition-all"
              placeholder="name@example.com"
              aria-required="true"
            />
          </div>

          <div>
            <label htmlFor="register-full-name" className="block text-sm font-semibold text-white drop-shadow mb-2">
              Полное имя
            </label>
            <input
              id="register-full-name"
              type="text"
              value={formData.full_name}
              onChange={handleChange('full_name')}
              className="w-full px-4 py-3 rounded-xl bg-transparent backdrop-blur-md border border-white/30 text-white placeholder:text-white/60 focus:outline-none focus:ring-2 focus:ring-white/50 focus:border-transparent transition-all"
              placeholder="Иван Иванов"
              autoComplete="name"
            />
          </div>

          <div>
            <label htmlFor="register-phone" className="block text-sm font-semibold text-white drop-shadow mb-2">
              Телефон
            </label>
            <input
              id="register-phone"
              type="tel"
              value={formData.phone}
              onChange={handleChange('phone')}
              className="w-full px-4 py-3 rounded-xl bg-transparent backdrop-blur-md border border-white/30 text-white placeholder:text-white/60 focus:outline-none focus:ring-2 focus:ring-white/50 focus:border-transparent transition-all"
              placeholder="+7 (999) 999-99-99"
              autoComplete="tel"
            />
          </div>

          <div>
            <label htmlFor="register-password" className="block text-sm font-semibold text-white drop-shadow mb-2">
              Пароль * (8-72 символа)
            </label>
            <input
              id="register-password"
              type="password"
              required
              minLength={8}
              maxLength={72}
              value={formData.password}
              onChange={handleChange('password')}
              className="w-full px-4 py-3 rounded-xl bg-transparent backdrop-blur-md border border-white/30 text-white placeholder:text-white/60 focus:outline-none focus:ring-2 focus:ring-white/50 focus:border-transparent transition-all"
              placeholder="Введите надёжный пароль"
              autoComplete="new-password"
              aria-required="true"
            />
          </div>

          <button
            type="submit"
            disabled={isLoading}
            onTouchEnd={handleTouchEnd}
            onKeyUp={handleKeyUp}
            className="btn-primary w-full text-base disabled:opacity-60 disabled:cursor-not-allowed disabled:transform-none"
          >
            {isLoading ? (
              <span className="flex items-center justify-center gap-2">
                <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                Регистрация...
              </span>
            ) : (
              'Зарегистрироваться'
            )}
          </button>
        </form>

        <div className="mt-8 text-center text-sm text-white/95">
          Уже есть аккаунт?{' '}
          <Link to="/login" className="text-amber-300 hover:text-amber-200 font-semibold transition-colors underline decoration-2 underline-offset-2">
            Войти
          </Link>
        </div>
        </div>
      </div>
    </div>
  )
}
