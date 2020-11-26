import React, { useReducer } from 'react';
import Root from './components/root';

import Context from './context';
import EditableTableContext from './editableTableContext';

import { EditableTableReducer, initEditableTableState } from './reducers/editableTableReducer';
import { Reducer, initialState } from './reducers/reducer';

const App = () => {

  const [state, dispatch] = useReducer(Reducer, initialState);
  const [editableTableState, editableTableDispatch] = useReducer(EditableTableReducer, initEditableTableState);

  const value = { state, dispatch };

  const editableTableValue = {
    state: editableTableState,
    dispatch: editableTableDispatch
  };

  return (
    <div className="App">
      <Context.Provider value={value}>
        <EditableTableContext.Provider value={editableTableValue}>
          <Root />
        </EditableTableContext.Provider>
      </Context.Provider>
    </div>
  )
}

export default App;
