/**
 * Astro Targets data for the Astro Targets page
 */

// Object Types (replaces userRoles)
export const objectTypes = [
    { id: 'nebula', name: 'Nebula', color: '' },
    { id: 'galaxy', name: 'Galaxy', color: '' },
    { id: 'cluster', name: 'Cluster', color: '' },
    // Add other types as needed
  ];
  

  
// Sort options
export const sortOptionsTargets = [
  { value: "name", label: "Name (A-Z)" },
  { value: "name-desc", label: "Name (Z-A)" },
  { value: "subs", label: "Subs (Low-High)" },
  { value: "subs-desc", label: "Subs (High-Low)" },
  { value: "const", label: "Constelation (Low-High)" },
  { value: "const-desc", label: "Constelation (High-Low)" }
];

  // Object Subtypes (replaces userStatuses)
  export const objectSubtypes = [
    { id: 'emission', name: 'Emission', color: 'text-orange-400' },
    { id: 'reflection', name: 'Reflection', color: 'text-purple-400' },
    { id: 'planetary', name: 'Planetary', color: 'text-teal-500' },
    { id: 'elliptical', name: 'Elliptical', color: 'text-blue-800' },
    { id: 'spiral', name: 'Spiral', color: 'text-blue-400' },
    { id: 'open', name: 'Open', color: 'text-gray-400' },
    { id: 'globular', name: 'Globular', color: 'text-yellow-400' }
    // Add other subtypes as needed
  ];
  
  // Sample DSO data (replaces users)
  export const dso = [
    {
      id: "1",
      object: "NGC 7635",
      name: "Bubble",
      type: "nebula", // Used for filtering (replaces 'role')
      subtype: "planetary", // Used for filtering (replaces 'status')
      size: "5",
      unit: "min",
      best: "sep,oct,nov",
      gear: "RedCat51 + ASI533MC + L-eNhance",
      subs: "120",
      integration: "8–15",
      constelation: "Cas",
      notes: "Emission shell around massive star; narrowband-like benefit",
      image_file: "NGC_7635.png",
      kanban_step: 0 // Used for departments in the original logic
    },
    {
      id: "2",
      object: "M13",
      name: "Hercules Globular Cluster",
      type: "cluster", // Used for filtering (replaces 'role')
      subtype: "globular", // Used for filtering (replaces 'status')
      size: "5",
      unit: "min",
      best: "sep,oct,nov",
      gear: "Askar91F + ASI585MC + L-Pro",
      subs: "240",
      integration: "8–15",
      constelation: "Her",
      notes: "Emission shell around massive star; narrowband-like benefit",
      image_file: "NGC_7635.png",
      kanban_step: 0 // Used for departments in the original logic  
    },
    {
      id: "3",
      object: "M45",
      name: "Seven Sisters",
      type: "cluster", // Used for filtering (replaces 'role')
      subtype: "open", // Used for filtering (replaces 'status')
      size: "5",
      unit: "min",
      best: "sep,oct,nov",
      gear: "Redcat51 + ASI585MC + L-Pro",
      subs: "120",
      integration: "8–15",
      constelation: "Tau",
      notes: "Emission shell around massive star; narrowband-like benefit",
      image_file: "NGC_7635.png",
      kanban_step: 1 // Used for departments in the original logic  
    },
        {
      id: "4",
      object: "NGC 7000",
      name: "North America Nebula",
      type: "nebula", // Used for filtering (replaces 'role')
      subtype: "emission", // Used for filtering (replaces 'status')
      size: "5",
      unit: "min",
      best: "sep,oct,nov",
      gear: "FMA180Pro + ASI533MC + L-eNhance",
      subs: "60",
      integration: "8–15",
      constelation: "Cyg",
      notes: "Emission shell around massive star; narrowband-like benefit",
      image_file: "NGC_7635.png",
      kanban_step: 2 // Used for departments in the original logic
    }
  ];



  
  // Target table columns
  export const targetColumns = [
    { key: 'object', label: 'Object', sortable: true },
    { key: 'name', label: 'Name', sortable: true },
    { key: 'type', label: 'Type', sortable: true },
    { key: 'subtype', label: 'Subtype', sortable: true },
    { key: 'size', label: 'Size', sortable: true },
    { key: 'best', label: 'Best Months', sortable: true },
    { key: 'integration', label: 'Integration Time', sortable: true },
    { key: 'kanban_step', label: 'Status Step', sortable: true }, // Replaces 'department'
    { key: 'gear', label: 'Gear', sortable: false }
    // { key: 'actions', label: 'Actions', sortable: false }
  ];
  

  export const kanbanSteps = [
    { key: 0, name: 'ToDo', outline_color: 'border-white-400' },
    { key: 1, name: 'Planning', outline_color: 'border-gray-400' },
    { key: 2, name: 'Starting' , outline_color: 'border-blue-400'},
    { key: 3, name: 'Imaging' , outline_color: 'border-yellow-400'},
    { key: 4, name: 'Processing' , outline_color: 'border-purple-400'},
    { key: 5, name: 'Reviewing' , outline_color: 'border-orange-400'},
    { key: 9, name: 'Completed', outline_color: 'border-green-400' }

  ];
  
  // Utility functions
  export function getStatusColor(status) {
    switch (status) {
      case 0:
        return 'badge border-white-400 badge-outline';
      case 1:
        return 'badge border-gray-400 badge-outline';
      case 2:
        return 'badge border-blue-400 badge-outline';
      case 3:
        return 'badge border-yellow-400 badge-outline';
      case 4:
        return 'badge border-purple-400 badge-outline';
      case 5:
        return 'badge border-orange-400 badge-outline';
      case 9:
        return 'badge border-green-400 badge-outline';
      default:
        return 'badge badge-neutral badge-outline';
    }
  }



export function getStatusDisplayText(status) {
  switch (status) {
    case 0:
      return 'ToDo';
    case 1:
      return 'Planning';
    case 2:
      return 'Starting';
    case 3:
      return 'Imaging';
    case 4:
      return 'Processing';
    case 5:
      return 'Reviewing';
    case 9:
      return 'Completed';
    default:
      return status;
  }
} 


export function getSubsColor(subs) {
  if (Number(subs) <= 60) return "text-teal-400";
  // between 61 and 120
  if (Number(subs) <= 120) return "text-yellow-400";
  // lower than 180
  if (Number(subs) <= 180) return "text-orange-400";
  // above 180
  if (Number(subs) > 180) return "text-red-400";
  return "text-success";
}