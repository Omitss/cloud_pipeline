import { useMutation } from '@tanstack/react-query'
import { login as loginApi, signup as signupApi } from '../api/authApi'
import { useAuth } from '../auth/AuthContext'

export function useLogin() {
  const { login } = useAuth()
  return useMutation({
    mutationFn: loginApi,
    onSuccess: login,
  })
}

export function useSignup() {
  const { login } = useAuth()
  return useMutation({
    mutationFn: signupApi,
    onSuccess: login, // 회원가입 성공 시 곧바로 로그인 상태로 전환
  })
}
