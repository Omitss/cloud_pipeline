import { AuthProvider } from './auth/AuthContext'
import Header from './components/Header'
import ImageSearchPage from './pages/ImageSearchPage'

function App() {
  return (
    <AuthProvider>
      <Header />
      <ImageSearchPage />
    </AuthProvider>
  )
}

export default App
