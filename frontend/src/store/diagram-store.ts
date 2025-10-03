/**
 * Diagram store for canvas state and diagram management
 */
import { create } from "zustand";
import { DiagramAPI } from "../services/diagram-api";
import type {
  Diagram,
  DiagramCreate,
  DiagramObject,
  DiagramObjectCreate,
  DiagramObjectUpdate,
  ObjectType,
  ApiError,
} from "../types/api";

interface DiagramState {
  // State
  diagrams: Diagram[];
  activeDiagram: Diagram | null;
  diagramObjects: DiagramObject[];
  canvasSettings: {
    zoom: number;
    pan: { x: number; y: number };
    gridEnabled: boolean;
    snapToGrid: boolean;
  };

  // UI State
  isLoading: boolean;
  error: string | null;

  // Actions - Diagrams
  loadDiagrams: () => Promise<void>;
  createDiagram: (data: DiagramCreate) => Promise<Diagram>;
  setActiveDiagram: (diagramId: number) => Promise<void>;
  updateDiagram: (
    id: number,
    name?: string,
    description?: string,
    tags?: string[]
  ) => Promise<void>;
  deleteDiagram: (id: number) => Promise<void>;
  clearActiveDiagram: () => void;

  // Actions - Diagram Objects
  addObject: (objectType: ObjectType, objectId: number, x: number, y: number) => Promise<void>;
  updateObjectPosition: (objectId: number, x: number, y: number) => Promise<void>;
  updateObjectStyle: (objectId: number, style: Record<string, any>) => Promise<void>;
  removeObject: (objectId: number) => Promise<void>;

  // Canvas Actions
  setZoom: (zoom: number) => void;
  setPan: (x: number, y: number) => void;
  setGridEnabled: (enabled: boolean) => void;
  setSnapToGrid: (enabled: boolean) => void;

  // Utility
  clearError: () => void;
}

export const useDiagramStore = create<DiagramState>((set, get) => ({
  // Initial state
  diagrams: [],
  activeDiagram: null,
  diagramObjects: [],
  canvasSettings: {
    zoom: 1,
    pan: { x: 0, y: 0 },
    gridEnabled: true,
    snapToGrid: true,
  },
  isLoading: false,
  error: null,

  // Diagrams
  loadDiagrams: async () => {
    set({ isLoading: true, error: null });
    try {
      const diagrams = await DiagramAPI.list();
      set({ diagrams, isLoading: false });
    } catch (err) {
      const apiError = err as ApiError;
      set({ error: apiError.message, isLoading: false });
    }
  },

  createDiagram: async (data: DiagramCreate) => {
    set({ isLoading: true, error: null });
    try {
      const diagram = await DiagramAPI.create(data);
      set((state) => ({
        diagrams: [...state.diagrams, diagram],
        isLoading: false,
      }));
      return diagram;
    } catch (err) {
      const apiError = err as ApiError;
      set({ error: apiError.message, isLoading: false });
      throw err;
    }
  },

  setActiveDiagram: async (diagramId: number) => {
    set({ isLoading: true, error: null });
    try {
      const diagram = await DiagramAPI.get(diagramId);

      // Load canvas settings from diagram if available
      const canvasSettings = diagram.canvas_settings || {
        zoom: 1,
        pan: { x: 0, y: 0 },
        gridEnabled: true,
        snapToGrid: true,
      };

      set({
        activeDiagram: diagram,
        canvasSettings,
        isLoading: false,
      });
    } catch (err) {
      const apiError = err as ApiError;
      set({ error: apiError.message, isLoading: false });
      throw err;
    }
  },

  updateDiagram: async (id: number, name?: string, description?: string, tags?: string[]) => {
    set({ isLoading: true, error: null });
    try {
      const updated = await DiagramAPI.update(id, { name, description, tags });
      set((state) => ({
        diagrams: state.diagrams.map((d) => (d.id === id ? updated : d)),
        activeDiagram: state.activeDiagram?.id === id ? updated : state.activeDiagram,
        isLoading: false,
      }));
    } catch (err) {
      const apiError = err as ApiError;
      set({ error: apiError.message, isLoading: false });
      throw err;
    }
  },

  deleteDiagram: async (id: number) => {
    set({ isLoading: true, error: null });
    try {
      await DiagramAPI.delete(id);
      set((state) => ({
        diagrams: state.diagrams.filter((d) => d.id !== id),
        activeDiagram: state.activeDiagram?.id === id ? null : state.activeDiagram,
        isLoading: false,
      }));
    } catch (err) {
      const apiError = err as ApiError;
      set({ error: apiError.message, isLoading: false });
      throw err;
    }
  },

  clearActiveDiagram: () => {
    set({ activeDiagram: null, diagramObjects: [] });
  },

  // Diagram Objects
  addObject: async (objectType: ObjectType, objectId: number, x: number, y: number) => {
    const { activeDiagram } = get();
    if (!activeDiagram) {
      set({ error: "No active diagram" });
      return;
    }

    set({ isLoading: true, error: null });
    try {
      const data: DiagramObjectCreate = {
        object_type: objectType,
        object_id: objectId,
        position_x: x,
        position_y: y,
      };

      const diagramObject = await DiagramAPI.addObject(activeDiagram.id, data);
      set((state) => ({
        diagramObjects: [...state.diagramObjects, diagramObject],
        isLoading: false,
      }));
    } catch (err) {
      const apiError = err as ApiError;
      set({ error: apiError.message, isLoading: false });
      throw err;
    }
  },

  updateObjectPosition: async (objectId: number, x: number, y: number) => {
    const { activeDiagram } = get();
    if (!activeDiagram) {
      set({ error: "No active diagram" });
      return;
    }

    set({ isLoading: true, error: null });
    try {
      const data: DiagramObjectUpdate = {
        position_x: x,
        position_y: y,
      };

      const updated = await DiagramAPI.updateObject(activeDiagram.id, objectId, data);
      set((state) => ({
        diagramObjects: state.diagramObjects.map((obj) => (obj.id === objectId ? updated : obj)),
        isLoading: false,
      }));
    } catch (err) {
      const apiError = err as ApiError;
      set({ error: apiError.message, isLoading: false });
      throw err;
    }
  },

  updateObjectStyle: async (objectId: number, style: Record<string, any>) => {
    const { activeDiagram } = get();
    if (!activeDiagram) {
      set({ error: "No active diagram" });
      return;
    }

    set({ isLoading: true, error: null });
    try {
      const data: DiagramObjectUpdate = {
        visual_style: style,
      };

      const updated = await DiagramAPI.updateObject(activeDiagram.id, objectId, data);
      set((state) => ({
        diagramObjects: state.diagramObjects.map((obj) => (obj.id === objectId ? updated : obj)),
        isLoading: false,
      }));
    } catch (err) {
      const apiError = err as ApiError;
      set({ error: apiError.message, isLoading: false });
      throw err;
    }
  },

  removeObject: async (objectId: number) => {
    const { activeDiagram } = get();
    if (!activeDiagram) {
      set({ error: "No active diagram" });
      return;
    }

    set({ isLoading: true, error: null });
    try {
      await DiagramAPI.removeObject(activeDiagram.id, objectId);
      set((state) => ({
        diagramObjects: state.diagramObjects.filter((obj) => obj.id !== objectId),
        isLoading: false,
      }));
    } catch (err) {
      const apiError = err as ApiError;
      set({ error: apiError.message, isLoading: false });
      throw err;
    }
  },

  // Canvas Actions
  setZoom: (zoom: number) => {
    set((state) => ({
      canvasSettings: { ...state.canvasSettings, zoom },
    }));
  },

  setPan: (x: number, y: number) => {
    set((state) => ({
      canvasSettings: { ...state.canvasSettings, pan: { x, y } },
    }));
  },

  setGridEnabled: (enabled: boolean) => {
    set((state) => ({
      canvasSettings: { ...state.canvasSettings, gridEnabled: enabled },
    }));
  },

  setSnapToGrid: (enabled: boolean) => {
    set((state) => ({
      canvasSettings: { ...state.canvasSettings, snapToGrid: enabled },
    }));
  },

  // Utility
  clearError: () => set({ error: null }),
}));
