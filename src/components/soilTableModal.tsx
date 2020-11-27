import React, { useContext, useEffect, useState } from 'react';
import { Button, Classes, Intent, Overlay } from '@blueprintjs/core';

import { setCells, setCellsLoadingState } from '../actions/editableTableAction';
import EditableTableContext from '../editableTableContext';

import SoilTable from './soilTable';
import SoilTableGraph from './soilTableGraph';


const SoilTableModal = () => {

  const { dispatch } = useContext(EditableTableContext);

  const [isOpen, setIsOpen] = useState(false);

  const handleOpen = () => setIsOpen(true);
  const handleClose = () => setIsOpen(false);

  useEffect(() => {
    fetch("/upload", { method: "POST" })
      .then(res => res.json())
      .then(data => {
        dispatch(setCells(data.data));
        dispatch(setCellsLoadingState(false));
      })
  }, [dispatch]);

  const overlayState = {
    autoFocus: true,
    canEscapeKeyClose: true,
    canOutsideClickClose: true,
    enforceFocus: true,
    hasBackdrop: true,
    usePortal: true,
    useTallContent: false,
  }

  return (
    <div>
      <Button onClick={handleOpen} />
      <Overlay onClose={handleClose} isOpen={isOpen} transitionDuration={0} {...overlayState}>
        <div className={Classes.CARD}>
          <div className="contents">
            <div className="col-1">
              <SoilTableGraph columnIndex={1} rowSize={23} />
            </div>
            <div className="col-2">
              <SoilTable columnWidth={80} numRows={32}/>
            </div>
          </div>
          <div>
            <Button intent={Intent.DANGER} onClick={handleClose} style={{ margin: "" }}>
              Close
            </Button>
          </div>
        </div>
      </Overlay>
    </div>
  );
};

export default SoilTableModal;
