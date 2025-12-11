import React from "react";

// grid: 2D array of symbols ("~", "O", "X", "M")
// onCellClick?: (row, col) => void
// fogOfWar?: boolean (hide ships)
const BoardGrid = ({ title, grid, onCellClick, fogOfWar = false }) => {
  if (!grid) {
    return (
      <div className="board-wrapper">
        <h3>{title}</h3>
        <div className="board-placeholder">No board yet</div>
      </div>
    );
  }

  const size = grid.length;

  const renderCellClass = (value) => {
    if (fogOfWar && value === "O") {
      value = "~";
    }
    switch (value) {
      case "O":
        return "cell cell-ship";
      case "X":
        return "cell cell-hit";
      case "M":
        return "cell cell-miss";
      default:
        return "cell cell-water";
    }
  };

  return (
    <div className="board-wrapper">
      <h3>{title}</h3>
      <div className="board-grid">
        <div className="board-header-row">
          <div className="corner" />
          {Array.from({ length: size }).map((_, col) => (
            <div key={col} className="header-cell">
              {col}
            </div>
          ))}
        </div>
        {grid.map((rowArr, row) => (
          <div key={row} className="board-row">
            <div className="header-cell">{row}</div>
            {rowArr.map((val, col) => (
              <button
                key={col}
                className={renderCellClass(val)}
                onClick={
                  onCellClick ? () => onCellClick(row, col) : undefined
                }
              />
            ))}
          </div>
        ))}
      </div>
    </div>
  );
};

export default BoardGrid;
