import styled from 'styled-components'

const Overlay = styled.div`
  position: fixed;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(15, 23, 42, 0.45);
  z-index: 50;
`

const Card = styled.div`
  position: relative;
  width: 100%;
  max-width: 360px;
  margin: 1rem;
  padding: 1.5rem;
  border-radius: 12px;
  background: #fff;
  box-shadow: 0 20px 40px rgba(15, 23, 42, 0.2);
`

const CloseButton = styled.button`
  position: absolute;
  top: 0.75rem;
  right: 0.9rem;
  border: none;
  background: none;
  font-size: 1.1rem;
  line-height: 1;
  color: #94a3b8;
  cursor: pointer;

  &:hover {
    color: #334155;
  }
`

function Modal({ onClose, children }) {
  return (
    <Overlay onClick={onClose}>
      <Card onClick={(e) => e.stopPropagation()}>
        <CloseButton type="button" onClick={onClose} aria-label="닫기">
          ✕
        </CloseButton>
        {children}
      </Card>
    </Overlay>
  )
}

export default Modal
