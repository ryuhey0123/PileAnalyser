// dispatchにactionを入れ込む
// そのactionはreducerでstateに変換される

import { Intent } from "@blueprintjs/core";
import { IAction, IState } from "../reducers/reducer";

export function solve(state: IState, dispatch: ((arg: IAction) => void)) {

  fetch("/solve", {
    method: "POST",
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(state.inputs)
  })
    .then((res) => res.json())
    .then((data) => {
      const action: IAction = {
        type: "output",
        outputs: data
      }
      dispatch(action);
    })
}

export function inputValueChange(key: string, value: number | string, dispatch: ((arg: IAction) => void)) {
  const action: IAction = {
    type: "input",
    inputs: { [key]: value },
  }
  dispatch(action)
}

const dataKey = (rowIndex: number, columnIndex: number) => {
  return `${rowIndex}-${columnIndex}`;
};

function isValidValue(value: string, columnIndex: number) {
  if (columnIndex === 2) {  // 土質
    return /^(S|C)$/.test(value);
  } if (columnIndex === 5) {  // alpha
    return /^(8|6)0$/.test(value);
  } else {
    return /^[0-9.]*$/.test(value);
  }
}

export function cellValidator(rowIndex: number, columnIndex: number, dispatch: ((arg: IAction) => void)) {
  const key = dataKey(rowIndex, columnIndex);
  return (value: string) => {
    const intent = isValidValue(value, columnIndex) ? "none" : Intent.DANGER;
    const action: IAction = {
      type: "setTable",
      soildata: {
        sparseCellIntent: { [key]: intent },
        sparseCellData: { [key]: value }
      }
    }
    dispatch(action)
  };
};

export function cellSetter(rowIndex: number, columnIndex: number, dispatch: ((arg: IAction) => void)) {
  const key = dataKey(rowIndex, columnIndex);
  return (value: string) => {
    const intent = isValidValue(value, columnIndex) ? "none" : Intent.DANGER;
    const action: IAction = {
      type: "setTable",
      soildata: {
        sparseCellIntent: { [key]: intent },
        sparseCellData: { [key]: value }
      }
    };
    dispatch(action);
  };
};

export function cellLoading(data: { [key: string]: string }, cellsLoadingIs: boolean, dispatch: ((arg: IAction) => void)) {
  const action: IAction = {
    type: "setTable",
    soildata: {
      sparseCellData: data,
      cellsLoading: cellsLoadingIs
    }
  };
  dispatch(action);
}
