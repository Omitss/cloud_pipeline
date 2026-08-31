import { useState } from 'react'
import { useSignup } from '../query/useAuthMutations'
import ErrorMessage from './ErrorMessage'
import { Form, Input, SubmitButton, SwitchText, Title } from './AuthFormElements'

function SignupForm({ onSuccess, onSwitchToLogin }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [nickname, setNickname] = useState('')
  const { mutate, isPending, isError, error } = useSignup()

  const handleSubmit = (e) => {
    e.preventDefault()
    mutate({ email, password, nickname }, { onSuccess })
  }

  return (
    <div>
      <Title>회원가입</Title>
      <Form onSubmit={handleSubmit}>
        <Input
          type="text"
          placeholder="닉네임"
          value={nickname}
          onChange={(e) => setNickname(e.target.value)}
          required
        />
        <Input
          type="email"
          placeholder="이메일"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <Input
          type="password"
          placeholder="비밀번호 (8자 이상)"
          value={password}
          minLength={8}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        {isError && <ErrorMessage message={error.message} />}
        <SubmitButton type="submit" disabled={isPending}>
          {isPending ? '가입 중...' : '회원가입'}
        </SubmitButton>
      </Form>
      <SwitchText>
        이미 계정이 있으신가요?{' '}
        <button type="button" onClick={onSwitchToLogin}>
          로그인
        </button>
      </SwitchText>
    </div>
  )
}

export default SignupForm
