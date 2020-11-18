import { createContext, Dispatch } from "react";
import { IResults, IState } from "./reducers/SolveReducer";

interface IContextProps {
    state: IState,
    dispatch: Dispatch<IResults>;
}

const Context = createContext({} as IContextProps);
export default Context;
