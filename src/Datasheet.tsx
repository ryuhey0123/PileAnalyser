import React, { useState } from 'react';
import ReactDataSheet from 'react-datasheet';
import styled from 'styled-components';

export interface GridElement extends ReactDataSheet.Cell<GridElement, number> {
    value: string | number | null;
}

class MyReactDataSheet extends ReactDataSheet<GridElement, number> { }

const cellRenderer: ReactDataSheet.CellRenderer<GridElement, number> = (props) => {
    const TableCell = styled.td`
        &.data-grid-container .data-grid .cell.read-only {
            background: black !important;
        }
        width: 100px;
        padding: 0;
        border: 1px solid black;
        & > span {
            display: block;
            border: 1px solid transparent;
        }
        &.selected {
            & > span {
                    display: block;
                    border: 1px solid green;
                    &:focus {
                        box-shadow: 0 0 5px 0 rgba(206, 40, 40, 0.5);
                }
            }
        }
        & > input {
            width: 100px;
            outline: none;
            border: none;
            &:focus {
                box-shadow: 0 0 5px 0 rgba(206, 40, 40, 0.5);
            }
        }
    `;

    return (
        <TableCell onMouseDown={props.onMouseDown} onMouseOver={props.onMouseOver} onDoubleClick={props.onDoubleClick}>
            {props.children}
        </TableCell>
    )
}


interface AppState {
    grid: GridElement[][];
}

function Datasheet() {
    const [state, setState] = useState<AppState>({
        grid: [
            [
              { readOnly: true, value: '' },
              { value: 'A', readOnly: true },
              { value: 'B', readOnly: true },
              { value: 'C', readOnly: true },
              { value: 'D', readOnly: true },
            ],
            [
              { readOnly: true, value: 1 },
              { value: 1 },
              { value: 3 },
              { value: 3 },
              { value: 3 },
            ],
            [
              { readOnly: true, value: 2 },
              { value: 2 },
              { value: 4 },
              { value: 4 },
              { value: 4 },
            ],
            [
              { readOnly: true, value: 3 },
              { value: 1 },
              { value: 3 },
              { value: 3 },
              { value: 3 },
            ],
            [
              { readOnly: true, value: 4 },
              { value: 2 },
              { value: 4 },
              { value: 4 },
              { value: 4 },
            ],
          ],
    });

    const valueRenderer = (cell: { value: any; }) => cell.value;

    const onCellsChanged = (changes: { cell: any; row: any; col: any; value: any; }[]) => {
        const grid = state.grid;
        changes.forEach(({ cell, row, col, value }) => {
          grid[row][col] = { ...grid[row][col], value };
        });
        setState({ grid });
      };


    return (
      <div className="sheet-container">
        <MyReactDataSheet
            data={state.grid}
            valueRenderer={valueRenderer}
            onCellsChanged={onCellsChanged}
            cellRenderer={cellRenderer}
        />
      </div>
    );
};

export default Datasheet;
