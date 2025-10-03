/**
 * Custom React-Flow edge for relationships with crow's foot notation
 * Shows cardinality at source and target ends
 */
import React from "react";
import { EdgeProps, getStraightPath } from "reactflow";
import type { Cardinality } from "../../types/api";

interface RelationshipEdgeData {
  sourceCardinality?: Cardinality;
  targetCardinality?: Cardinality;
  label?: string;
}

/**
 * Get crow's foot symbol for cardinality
 */
const getCardinalitySymbol = (cardinality?: Cardinality): string => {
  switch (cardinality) {
    case "ONE":
      return "1"; // 1..1
    case "ZERO_ONE":
      return "0..1"; // 0..1
    case "ONE_MANY":
      return "1..*"; // 1..N
    case "ZERO_MANY":
      return "*"; // 0..N
    default:
      return "";
  }
};

export const RelationshipEdge: React.FC<EdgeProps<RelationshipEdgeData>> = ({
  id,
  sourceX,
  sourceY,
  targetX,
  targetY,
  sourcePosition,
  targetPosition,
  data,
  markerEnd,
}) => {
  const [edgePath] = getStraightPath({
    sourceX,
    sourceY,
    sourcePosition,
    targetX,
    targetY,
    targetPosition,
  });

  const sourceLabel = getCardinalitySymbol(data?.sourceCardinality);
  const targetLabel = getCardinalitySymbol(data?.targetCardinality);

  // Calculate label positions
  const sourceLabelX = sourceX + (targetX - sourceX) * 0.25;
  const sourceLabelY = sourceY + (targetY - sourceY) * 0.25;
  const targetLabelX = sourceX + (targetX - sourceX) * 0.75;
  const targetLabelY = sourceY + (targetY - sourceY) * 0.75;

  return (
    <>
      <path
        id={id}
        className="react-flow__edge-path relationship-edge"
        d={edgePath}
        markerEnd={markerEnd}
        strokeWidth={2}
        stroke="#555"
      />

      {/* Source cardinality label */}
      {sourceLabel && (
        <text
          x={sourceLabelX}
          y={sourceLabelY}
          className="edge-label source-cardinality"
          textAnchor="middle"
          dominantBaseline="middle"
        >
          {sourceLabel}
        </text>
      )}

      {/* Target cardinality label */}
      {targetLabel && (
        <text
          x={targetLabelX}
          y={targetLabelY}
          className="edge-label target-cardinality"
          textAnchor="middle"
          dominantBaseline="middle"
        >
          {targetLabel}
        </text>
      )}

      {/* Relationship label (optional) */}
      {data?.label && (
        <text
          x={(sourceX + targetX) / 2}
          y={(sourceY + targetY) / 2}
          className="edge-label relationship-label"
          textAnchor="middle"
          dominantBaseline="middle"
        >
          {data.label}
        </text>
      )}
    </>
  );
};
