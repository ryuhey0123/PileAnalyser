import { createContext, Dispatch } from "react";
import { EditableTableAction } from "./actions/editableTableAction";
import { EditableTableState } from "./reducers/editableTableReducer";


interface EditableTableContextProps {
  state: EditableTableState,
  dispatch: Dispatch<EditableTableAction>;
};

const EditableTableContext = createContext({} as EditableTableContextProps);
export default EditableTableContext;
