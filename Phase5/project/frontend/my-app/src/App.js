import './App.css';
import EventsList from './components/eventlist';
import LoginForm from './components/login';
import Signup from './components/signup';

function App() {
  return(
    <Signup />,
    <LoginForm/>,
    <EventsList />
  )
}

export default App;
