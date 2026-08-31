import { useState } from 'react'
import styled from 'styled-components'
import { useAuth } from '../auth/AuthContext'
import Modal from './Modal'
import LoginForm from './LoginForm'
import SignupForm from './SignupForm'

const Bar = styled.header`
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1.5rem;
  border-bottom: 1px solid #e2e8f0;
  background: #fff;
`

const Brand = styled.span`
  font-weight: 700;
  color: #1e293b;
`

const Actions = styled.div`
  display: flex;
  align-items: center;
  gap: 0.75rem;
`

const Greeting = styled.span`
  font-size: 0.9rem;
  color: #475569;

  strong {
    color: #1e293b;
  }
`

const TextButton = styled.button`
  padding: 0.4rem 0.9rem;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  background: #fff;
  color: #334155;
  font-size: 0.85rem;
  cursor: pointer;

  &:hover {
    background: #f8fafc;
  }
`

const PrimaryTextButton = styled(TextButton)`
  border-color: #4f46e5;
  color: #4f46e5;
`

function Header() {
  const { user, logout } = useAuth()
  const [modal, setModal] = useState(null) // 'login' | 'signup' | null

  return (
    <Bar>
      <Brand>imageRag</Brand>
      <Actions>
        {user ? (
          <>
            <Greeting>
              <strong>{user.nickname}</strong>님 안녕하세요
            </Greeting>
            <TextButton type="button" onClick={logout}>
              로그아웃
            </TextButton>
          </>
        ) : (
          <>
            <TextButton type="button" onClick={() => setModal('login')}>
              로그인
            </TextButton>
            <PrimaryTextButton type="button" onClick={() => setModal('signup')}>
              회원가입
            </PrimaryTextButton>
          </>
        )}
      </Actions>

      {modal && (
        <Modal onClose={() => setModal(null)}>
          {modal === 'login' ? (
            <LoginForm onSuccess={() => setModal(null)} onSwitchToSignup={() => setModal('signup')} />
          ) : (
            <SignupForm onSuccess={() => setModal(null)} onSwitchToLogin={() => setModal('login')} />
          )}
        </Modal>
      )}
    </Bar>
  )
}

export default Header
