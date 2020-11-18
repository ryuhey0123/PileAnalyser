import React, { useReducer } from 'react';
import Root from './components/Root';
import Context from './Context';
import { AppReducer, initialState } from './reducers/SolveReducer';

const App = () => {

    const [state, dispatch] = useReducer(AppReducer, initialState);
    const value = { state, dispatch };

    return (
        <div className="App">
            <Context.Provider value={value}>
                <Root/>
            </Context.Provider>
        </div>
    )
}

export default App;
