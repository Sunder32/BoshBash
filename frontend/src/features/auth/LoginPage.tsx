import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuthStore } from '../../store/authStore'
import { AlertCircle, Shield, Zap, Users, Sparkles } from 'lucide-react'

export default function LoginPage() {
  const navigate = useNavigate()
  const { login, isLoading, error, clearError } = useAuthStore()
  
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    clearError()
    
    try {
      await login(formData)
      navigate('/')
    } catch (err) {
    }
  }

  return (
    <div className="min-h-screen relative flex items-center justify-center px-4 py-12 bg-slate-950 text-slate-100">
      {/* Emergency lights */}
      <div className="emergency-light-red" style={{ top: '10%', left: '10%' }} />
      <div className="emergency-light-blue" style={{ bottom: '10%', right: '10%' }} />

      <div className="relative z-10 w-full max-w-6xl">
        <div className="aurora-wrapper rounded-[3rem] bg-slate-900/40 border border-white/10 shadow-[0_40px_80px_-45px_rgba(15,23,42,0.9)]">
          <div className="absolute inset-0 overflow-hidden rounded-[3rem]">
            <div className="absolute -top-24 -right-24 w-64 h-64 bg-gradient-to-br from-amber-400/40 via-rose-500/30 to-purple-500/40 blur-[120px]" />
            <div className="absolute bottom-0 left-1/3 w-80 h-80 bg-gradient-to-tr from-blue-500/30 via-sky-400/20 to-rose-400/40 blur-[140px]" />
          </div>

          <div className="relative grid gap-12 lg:grid-cols-[1.05fr_0.95fr] p-6 sm:p-12">
            {/* Hero Section */}
            <div className="flex flex-col justify-between">
              <div className="space-y-8">
                <div className="inline-flex items-center gap-3 bg-white/10 border border-white/20 px-4 py-2 rounded-full text-sm font-medium uppercase tracking-[0.3em] text-white/80 w-fit shadow-lg">
                  <Sparkles className="w-4 h-4" />
                  Rescue Operations Cloud
                </div>

                <div className="space-y-5">
                  <div className="inline-flex items-center justify-center w-20 h-20 rounded-[2rem] bg-white text-4xl shadow-[0_20px_60px_rgba(255,255,255,0.35)]">
                    🚨
                  </div>
                  <h1 className="text-3xl sm:text-4xl xl:text-5xl font-semibold leading-tight text-white drop-shadow-2xl">
                    Экосистема спасательных операций следующего поколения
                  </h1>
                  <p className="text-sm sm:text-base text-slate-100/80 max-w-xl leading-relaxed">
                    Отправляйте SOS, отслеживайте статус спасателей и получайте советы в едином интерфейсе.
                    Всё защищено, быстро и доступно 24/7.
                  </p>
                </div>

                <div className="grid gap-3 sm:grid-cols-3">
                  <div className="glass-card-dark rounded-xl p-4 border border-white/10 shadow-xl">
                    <Shield className="w-6 h-6 text-emerald-300 mb-2" />
                    <p className="text-[10px] uppercase tracking-[0.2em] text-white/60">Безопасность</p>
                    <p className="text-base font-semibold">ISO/IEC 27001</p>
                  </div>
                  <div className="glass-card-dark rounded-xl p-4 border border-white/10 shadow-xl">
                    <Zap className="w-6 h-6 text-amber-300 mb-2" />
                    <p className="text-[10px] uppercase tracking-[0.2em] text-white/60">Скорость</p>
                    <p className="text-base font-semibold">до 1.2 сек</p>
                  </div>
                  <div className="glass-card-dark rounded-xl p-4 border border-white/10 shadow-xl">
                    <Users className="w-6 h-6 text-sky-300 mb-2" />
                    <p className="text-[10px] uppercase tracking-[0.2em] text-white/60">Надёжность</p>
                    <p className="text-base font-semibold">24/7/365</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Login Side */}
            <div className="relative flex">
              <div className="p-8 sm:p-10 backdrop-blur-2xl bg-white/5 rounded-3xl border border-white/20 shadow-2xl flex flex-col h-full w-full min-h-[600px]">
                <div>
                  <p className="section-title text-white/90">Войти в систему</p>
                  <h2 className="mt-3 text-2xl sm:text-3xl font-semibold text-white drop-shadow-lg">
                    Управление инцидентами и аналитика в одном окне
                  </h2>
                  <p className="mt-2 text-sm text-white/90 drop-shadow">
                    Используйте корпоративный аккаунт, чтобы получить доступ к панели управления и последним тревогам.
                  </p>
                </div>

                <div className="flex-1 flex flex-col justify-center">
                  {error && (
                    <div className="mb-6 bg-rose-50 border border-rose-200 text-rose-700 px-4 py-3 rounded-2xl flex items-center gap-3 animate-fade-in">
                      <AlertCircle className="w-5 h-5 flex-shrink-0" />
                      <span className="text-sm font-medium">{error}</span>
                    </div>
                  )}

                  <form onSubmit={handleSubmit} className="space-y-6 w-full">
                    <div className="space-y-2">
                      <label htmlFor="email" className="block text-sm font-semibold text-white drop-shadow">
                        Email адрес
                      </label>
                      <input
                        id="email"
                        type="email"
                        required
                        autoComplete="email"
                        value={formData.email}
                        onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                        className="w-full px-4 py-3 rounded-xl bg-transparent backdrop-blur-md border border-white/30 text-white placeholder:text-white/60 focus:outline-none focus:ring-2 focus:ring-white/50 focus:border-transparent transition-all"
                        placeholder="dispatcher@rescue.ru"
                      />
                    </div>

                    <div className="space-y-2">
                      <label htmlFor="password" className="block text-sm font-semibold text-white drop-shadow">
                        Пароль
                      </label>
                      <input
                        id="password"
                        type="password"
                        required
                        autoComplete="current-password"
                        value={formData.password}
                        onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                        className="w-full px-4 py-3 rounded-xl bg-transparent backdrop-blur-md border border-white/30 text-white placeholder:text-white/60 focus:outline-none focus:ring-2 focus:ring-white/50 focus:border-transparent transition-all"
                        placeholder="Введите пароль"
                      />
                    </div>

                    <button
                      type="submit"
                      disabled={isLoading}
                      className="btn-primary w-full text-base disabled:opacity-60 disabled:cursor-not-allowed disabled:transform-none"
                    >
                      {isLoading ? (
                        <span className="flex items-center justify-center gap-2 pointer-events-none">
                          <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 714 12H0c0 3.042 1.135 5.824 3 7.938л3-2.647z" />
                          </svg>
                          Вход...
                        </span>
                      ) : (
                        'Войти в систему'
                      )}
                    </button>
                  </form>
                </div>

                <div className="pt-6 text-center text-sm text-white/95">
                  Нет аккаунта?{' '}
                  <Link
                    to="/register"
                    className="text-amber-300 hover:text-amber-200 font-semibold transition-colors underline decoration-2 underline-offset-2"
                  >
                    Зарегистрироваться
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
