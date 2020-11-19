import React, { useReducer } from 'react';
import Root from './components/Root';
import Context from './Context';
import { Reducer, initialState } from './reducers/Reducer';

const App = () => {

    const [state, dispatch] = useReducer(Reducer, initialState);
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
