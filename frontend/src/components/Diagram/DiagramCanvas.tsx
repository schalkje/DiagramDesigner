/**
 * Diagram Canvas using React-Flow
 * Displays entities as nodes and relationships as edges with crow's foot notation
 */
import React, { useCallback, useEffect, useMemo } from "react";
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  Node,
  Edge,
  Connection,
  useNodesState,
  useEdgesState,
  addEdge,
  BackgroundVariant,
} from "reactflow";
import "reactflow/dist/style.css";
import { useDiagramStore } from "../../store";
import { EntityNode } from "./EntityNode";
import { RelationshipEdge } from "./RelationshipEdge";
import type { Entity, ObjectType } from "../../types/api";

interface DiagramCanvasProps {
  diagramId: number;
}

export const DiagramCanvas: React.FC<DiagramCanvasProps> = ({ diagramId }) => {
  const {
    activeDiagram,
    diagramObjects,
    setActiveDiagram,
    addObject,
    updateObjectPosition,
    canvasSettings,
    setZoom,
    setPan,
  } = useDiagramStore();

  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  // Custom node types
  const nodeTypes = useMemo(() => ({ entityNode: EntityNode }), []);

  // Custom edge types
  const edgeTypes = useMemo(() => ({ relationshipEdge: RelationshipEdge }), []);

  // Load diagram on mount
  useEffect(() => {
    setActiveDiagram(diagramId);
  }, [diagramId, setActiveDiagram]);

  // Convert diagram objects to React-Flow nodes
  useEffect(() => {
    if (!diagramObjects) return;

    const flowNodes: Node[] = diagramObjects.map((obj) => ({
      id: `object-${obj.id}`,
      type: "entityNode",
      position: { x: obj.position_x, y: obj.position_y },
      data: {
        objectId: obj.object_id,
        objectType: obj.object_type,
        label: `Entity ${obj.object_id}`, // Will be replaced by EntityNode component
        style: obj.visual_style,
      },
    }));

    setNodes(flowNodes);
  }, [diagramObjects, setNodes]);

  // Handle node drag end - update position in backend
  const onNodeDragStop = useCallback(
    (_event: React.MouseEvent, node: Node) => {
      const objectId = parseInt(node.id.replace("object-", ""));
      updateObjectPosition(objectId, node.position.x, node.position.y);
    },
    [updateObjectPosition]
  );

  // Handle drop from repository tree
  const onDrop = useCallback(
    (event: React.DragEvent) => {
      event.preventDefault();

      const entityData = event.dataTransfer.getData("application/json");
      if (!entityData) return;

      const entity: Entity = JSON.parse(entityData);
      const reactFlowBounds = (event.target as HTMLElement).getBoundingClientRect();

      // Calculate position relative to canvas
      const position = {
        x: event.clientX - reactFlowBounds.left,
        y: event.clientY - reactFlowBounds.top,
      };

      // Add entity to diagram
      addObject("ENTITY" as ObjectType, entity.id, position.x, position.y);
    },
    [addObject]
  );

  const onDragOver = useCallback((event: React.DragEvent) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = "copy";
  }, []);

  // Handle connection (creating relationships)
  const onConnect = useCallback(
    (params: Connection) => {
      // TODO: Implement relationship creation
      setEdges((eds) => addEdge({ ...params, type: "relationshipEdge" }, eds));
    },
    [setEdges]
  );

  if (!activeDiagram) {
    return <div className="diagram-canvas loading">Loading diagram...</div>;
  }

  return (
    <div
      className="diagram-canvas"
      onDrop={onDrop}
      onDragOver={onDragOver}
      style={{ width: "100%", height: "100%" }}
    >
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onNodeDragStop={onNodeDragStop}
        onConnect={onConnect}
        nodeTypes={nodeTypes}
        edgeTypes={edgeTypes}
        fitView
        defaultZoom={canvasSettings.zoom}
        defaultViewport={{
          x: canvasSettings.pan.x,
          y: canvasSettings.pan.y,
          zoom: canvasSettings.zoom,
        }}
        snapToGrid={canvasSettings.snapToGrid}
        snapGrid={[15, 15]}
      >
        <Background
          variant={canvasSettings.gridEnabled ? BackgroundVariant.Dots : BackgroundVariant.Lines}
          gap={15}
          size={1}
        />
        <Controls />
        <MiniMap nodeColor="#4CAF50" />
      </ReactFlow>
    </div>
  );
};
