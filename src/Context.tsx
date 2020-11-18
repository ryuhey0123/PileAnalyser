import { createContext, Dispatch } from "react";
import { IResult, IState } from "./reducers/SolveReducer";

interface IContextProps {
    state: IState,
    dispatch: Dispatch<IResult[]>;
}

const Context = createContext({} as IContextProps);
export default Context;
