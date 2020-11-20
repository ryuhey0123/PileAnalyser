// actionをstateに変換
// イコールDispatch
import { Intent } from "@blueprintjs/core";

export interface IInputs {
  [key: string]: number | string
}

export interface IOutputs {
  results: { [key: string]: number }[]
  time: string
}

export interface ISoilData {
  [key: string]: any,
  columnNames?: string[];
  sparseCellData?: { [key: string]: string };
  sparseCellIntent?: { [key: string]: Intent };
  sparseColumnIntents?: Intent[];
  cellsLoading?: boolean;
}

export interface IState {
  inputs: IInputs,
  outputs: IOutputs,
  soildata: ISoilData,
}

export interface IAction {
  type: "input" | "output" | "setTable",
  inputs?: IInputs,
  outputs?: IOutputs,
  soildata?: ISoilData,
}

export const initialState: IState = {
  inputs: {
    mode: "non_liner_multi",
    bottom_condition: "pin",
    material: "concrete",
    condition: 1.0,
    diameter: 1300,
    length: 17.5,
    level: -2.5,
    force: 500,
  },
  outputs: {
    results: [{}],
    time: ""
  },
  soildata: {
    columnNames: ["深度", "N値", "土質", "低減係数", "採用低減係数", "α", "E0"],
    sparseCellData: {},
    sparseCellIntent: {},
    sparseColumnIntents: [],
    cellsLoading: true
  }
}

export function Reducer(preState: IState, action: IAction) {
  switch (action.type) {

    case "output":
      const newOutState: IState = {
        inputs: preState.inputs,
        outputs: action.outputs!,
        soildata: preState.soildata
      }
      return newOutState

    case "input":
      const newInState: IState = {
        inputs: preState.inputs,
        outputs: preState.outputs,
        soildata: preState.soildata
      }
      for (const key in action.inputs) {
        newInState.inputs[key] = action.inputs[key];
      };
      return newInState

    case "setTable":
      const newTableState: IState = {
        inputs: preState.inputs,
        outputs: preState.outputs,
        soildata: preState.soildata
      }
      if (action.soildata?.sparseCellData) {
        for (const dataKey in action.soildata.sparseCellData) {
          newTableState.soildata.sparseCellData![dataKey] = action.soildata.sparseCellData![dataKey];
          newTableState.soildata.cellsLoading = false;
        }
      }
      if (action.soildata?.sparseCellIntent) {
        for (const dataKey in action.soildata.sparseCellIntent) {
          newTableState.soildata.sparseCellIntent![dataKey] = action.soildata.sparseCellIntent![dataKey];
        }
      }
      else {
        for (const key in action.soildata) {
          newTableState.soildata[key] = action.soildata[key];
        }
      }
      return newTableState
  }
}
