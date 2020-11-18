import React, { useReducer } from 'react';
import { AppContext } from './contexts/Context';
import { AppReducer } from './reducers/Reducer';

function App() {
    const initialState = {
        isState: Array(10).fill(false)
    }
    const [state, dispatch] = useReducer(AppReducer, initialState);

    return (
        <div className="App">
            <AppContext.Provider value={{state, dispatch}}>
            </AppContext.Provider>
        </div>
    )
}

export default App;
