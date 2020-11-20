import React, { useReducer } from 'react';
import Root from './components/root';
import Context from './context';
import { Reducer, initialState } from './reducers/reducer';

const App = () => {

  const [state, dispatch] = useReducer(Reducer, initialState);
  const value = { state, dispatch };

  return (
    <div className="App">
      <Context.Provider value={value}>
        <Root />
      </Context.Provider>
    </div>
  )
}

export default App;
