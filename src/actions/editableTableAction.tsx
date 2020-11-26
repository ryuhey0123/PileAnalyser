export enum EditableTableActionType {
  SET_CELLS,
  SET_CELLS_LOADING_STATE
}

export interface EditableTableAction {
  type: EditableTableActionType,
  payload: any,
  meta?: any,
  error?: any
}

export const setCells = (cells: { [key: string]: string }): EditableTableAction => ({
  type: EditableTableActionType.SET_CELLS,
  payload: cells
});

export const setCellsLoadingState = (bool: boolean): EditableTableAction => ({
  type: EditableTableActionType.SET_CELLS_LOADING_STATE,
  payload: bool
})
