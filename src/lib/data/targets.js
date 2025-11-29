/**
 * Astro Targets data for the Astro Targets page
 */

// Object Types (replaces userRoles)
export const objectTypes = [
    { id: 'nebula', name: 'Nebula', color: 'bg-error/20 text-error' },
    { id: 'galaxy', name: 'Galaxy', color: 'bg-primary/20 text-primary' },
    // Add other types as needed
  ];
  
  // Object Subtypes (replaces userStatuses)
  export const objectSubtypes = [
    { id: 'emission', name: 'Emission', color: 'bg-success/20 text-success' },
    { id: 'reflection', name: 'Reflection', color: 'bg-warning/20 text-warning' },
    { id: 'planetary', name: 'Planetary', color: 'bg-info/20 text-info' },
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
      subs: "240",
      integration: "8–15",
      notes: "Emission shell around massive star; narrowband-like benefit",
      image_file: "NGC_7635.png",
      kanban_step: "0" // Used for departments in the original logic
    }
    // Add more DSO objects here
  ];
  
  // Departments (replaces departments, using 'kanban_step' to maintain filter structure)
  // Since kanban_step is a number, we'll map it for the filter dropdown
  export const kanbanSteps = [
    '0', // Example: Planning
    '1', // Example: Scheduled
    '2', // Example: Captured
    '3'  // Example: Processed
  ];
  
  // Target table columns (replaces userColumns)
  export const targetColumns = [
    { key: 'object', label: 'Object', sortable: true },
    { key: 'name', label: 'Name', sortable: true },
    { key: 'type', label: 'Type', sortable: true },
    { key: 'subtype', label: 'Subtype', sortable: true },
    { key: 'size', label: 'Size', sortable: true },
    { key: 'best', label: 'Best Months', sortable: true },
    { key: 'integration', label: 'Integration Time', sortable: true },
    { key: 'kanban_step', label: 'Status Step', sortable: true }, // Replaces 'department'
    { key: 'actions', label: 'Actions', sortable: false }
  ];
  
  // Target statistics (replaces userStats)
  export const targetStats = [
    {
      name: 'Total Targets',
      value: dso.length.toString(),
      change: '+0', // Placeholder
      changeType: 'positive',
      icon: 'heroicons:star'
    },
    {
      name: 'Nebulae',
      value: dso.filter(target => target.type === 'nebula').length.toString(),
      change: '+0',
      changeType: 'positive',
      icon: 'heroicons:fire'
    },
    {
      name: 'Galaxies',
      value: dso.filter(target => target.type === 'galaxy').length.toString(),
      change: '+0',
      changeType: 'positive',
      icon: 'heroicons:chart-bar'
    },
    {
      name: 'Processed Targets',
      value: dso.filter(target => target.kanban_step === '3').length.toString(),
      change: '+0',
      changeType: 'positive',
      icon: 'heroicons:document-text'
    }
  ];