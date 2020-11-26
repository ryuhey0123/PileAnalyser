import { createContext, Dispatch } from "react";
import { IAction, IState } from "./reducers/reducer";

interface IContextProps {
  state: IState,
  dispatch: Dispatch<IAction>;
}

const Context = createContext({} as IContextProps);
export default Context;

