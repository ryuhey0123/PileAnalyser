import { EditableTableAction, EditableTableActionType } from "../actions/editableTableAction";

export interface EditableTableState {
  tableData: {
    sparseCellData?: { [key: string]: string },
    cellsLoading?: boolean,
  },
  graphData: {
    nValues?: [ {x: number, nValue: number} ]
  }
}

export const initEditableTableState: EditableTableState = {
  tableData: {
    sparseCellData: {},
    cellsLoading: true,
  },
  graphData: {
    nValues: [ {x: 1, nValue: 1} ],
  }
}


export function EditableTableReducer(preState: EditableTableState, action: EditableTableAction) {

  switch (action.type) {

    case EditableTableActionType.SET_CELLS: {
      const newState: EditableTableState = {...preState};
      if (newState.tableData.sparseCellData) {
        for (const key in action.payload) {
          newState.tableData.sparseCellData[key] = action.payload[key];
        };
      }
      return newState
    }

    case EditableTableActionType.SET_CELLS_LOADING_STATE: {
      const newState: EditableTableState = {...preState};
      newState.tableData.cellsLoading = action.payload;
      return newState
    }

  }
}
