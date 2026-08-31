import styled from 'styled-components'

export const Title = styled.h2`
  margin: 0 0 1rem;
  font-size: 1.2rem;
`

export const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
`

export const Input = styled.input`
  padding: 0.6rem 0.75rem;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  font-size: 0.9rem;
`

export const SubmitButton = styled.button`
  padding: 0.6rem;
  border: none;
  border-radius: 6px;
  background: #4f46e5;
  color: #fff;
  font-weight: 600;
  cursor: pointer;

  &:disabled {
    background: #c7d2fe;
    cursor: not-allowed;
  }

  &:hover:not(:disabled) {
    background: #4338ca;
  }
`

export const SwitchText = styled.p`
  margin: 0.75rem 0 0;
  font-size: 0.85rem;
  color: #64748b;
  text-align: center;

  button {
    padding: 0;
    border: none;
    background: none;
    color: #4f46e5;
    font-weight: 600;
    cursor: pointer;
  }
`
