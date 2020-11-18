import { createContext, Dispatch } from "react";
import { IOutput, IState } from "./reducers/SolveReducer";

interface IContextProps {
    state: IState,
    dispatch: Dispatch<IOutput[]>;
}

const Context = createContext({} as IContextProps);
export default Context;
