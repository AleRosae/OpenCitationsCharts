import logo from './logo.svg';
import './App.css';
import NavBar from './components/NavBar'
import MainPage from './components/MainPage'
import StartVis from './components/StartVis'
import CreatePage from './components/CreatePage';

function App() {
  return (
    <div className="App">
      <NavBar />

      <MainPage />

      <StartVis />

      <CreatePage title='Questo titolo' text = 'un sacco di testo che spiega cose' />
    </div>
  );
}

export default App;
