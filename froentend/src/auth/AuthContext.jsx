import { createContext, useCallback, useContext, useEffect, useState } from 'react'
import { useQuery, useQueryClient } from '@tanstack/react-query'
import { fetchMe } from '../api/authApi'

const AuthContext = createContext(null)
const TOKEN_KEY = 'accessToken'

export function AuthProvider({ children }) {
  const [accessToken, setAccessTokenState] = useState(() => localStorage.getItem(TOKEN_KEY))
  const queryClient = useQueryClient()

  const setAccessToken = useCallback((token) => {
    if (token) {
      localStorage.setItem(TOKEN_KEY, token)
    } else {
      localStorage.removeItem(TOKEN_KEY)
    }
    setAccessTokenState(token)
  }, [])

  const { data: user, isError } = useQuery({
    queryKey: ['me', accessToken],
    queryFn: () => fetchMe(accessToken),
    enabled: !!accessToken,
    retry: false,
  })

  const logout = useCallback(() => {
    setAccessToken(null)
    queryClient.removeQueries({ queryKey: ['me'] })
  }, [queryClient, setAccessToken])

  // access token 만료/무효화로 /auth/me가 실패하면 그냥 로그아웃 처리한다 (자동 재발급 없음).
  useEffect(() => {
    if (accessToken && isError) {
      logout()
    }
  }, [accessToken, isError, logout])

  const login = useCallback(
    (tokens) => {
      setAccessToken(tokens.access_token)
      queryClient.setQueryData(['me', tokens.access_token], tokens.user)
    },
    [queryClient, setAccessToken],
  )

  const value = {
    user: accessToken ? user ?? null : null,
    login,
    logout,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth는 AuthProvider 안에서만 사용할 수 있습니다.')
  return ctx
}
