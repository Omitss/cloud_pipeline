import styled, { keyframes } from 'styled-components'

const spin = keyframes`
  to {
    transform: rotate(360deg);
  }
`

const Spinner = styled.div`
  width: 32px;
  height: 32px;
  margin: 1rem auto;
  border: 3px solid #e2e8f0;
  border-top-color: #4f46e5;
  border-radius: 50%;
  animation: ${spin} 0.8s linear infinite;
`

function LoadingSpinner() {
  return <Spinner role="status" aria-label="검색 중" />
}

export default LoadingSpinner
