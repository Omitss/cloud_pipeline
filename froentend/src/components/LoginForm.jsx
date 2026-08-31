import { useState } from 'react'
import { useLogin } from '../query/useAuthMutations'
import ErrorMessage from './ErrorMessage'
import { Form, Input, SubmitButton, SwitchText, Title } from './AuthFormElements'

function LoginForm({ onSuccess, onSwitchToSignup }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const { mutate, isPending, isError, error } = useLogin()

  const handleSubmit = (e) => {
    e.preventDefault()
    mutate({ email, password }, { onSuccess })
  }

  return (
    <div>
      <Title>로그인</Title>
      <Form onSubmit={handleSubmit}>
        <Input
          type="email"
          placeholder="이메일"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <Input
          type="password"
          placeholder="비밀번호"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        {isError && <ErrorMessage message={error.message} />}
        <SubmitButton type="submit" disabled={isPending}>
          {isPending ? '로그인 중...' : '로그인'}
        </SubmitButton>
      </Form>
      <SwitchText>
        계정이 없으신가요?{' '}
        <button type="button" onClick={onSwitchToSignup}>
          회원가입
        </button>
      </SwitchText>
    </div>
  )
}

export default LoginForm
