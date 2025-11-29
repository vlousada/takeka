<script>
    import { onMount } from "svelte";
    import Icon from "@iconify/svelte";
    import { _ } from "svelte-i18n";
  
    // 🛑 UPDATED: Import data from the new 'targets.js' file
    import {
      dso,
      targetStats,
      objectTypes, // Replaces userRoles
      objectSubtypes, // Replaces userStatuses
      kanbanSteps, // Replaces departments
      targetColumns,
    } from "../data/targets.js"; 
    
    // NOTE: You'll need to create dummy files for avatar generation or remove them
    import {
      generateUserAvatar, // Keep for now, but will use target name
      generateFallbackAvatar,
    } from "../utils/avatar.js";
    
    import {
      motionInView,
      staggerAnimate,
      motionHover,
    } from "../utils/motion.js";
    import DeleteConfirmationModal from "../components/DeleteConfirmationModal.svelte";
  
    // 🛑 UPDATED: Variable names changed from 'user' to 'target'
    let filteredTargets = [...dso]; 
    let searchTerm = "";
    let selectedType = ""; // Replaces selectedRole
    let selectedSubtype = ""; // Replaces selectedStatus
    let selectedKanbanStep = ""; // Replaces selectedDepartment
    let sortBy = "name";
    let sortDirection = "asc";
    let showAddTargetModal = false;
    let selectedTarget = null;
    let showTargetModal = false;
    let showDeleteModal = false;
    let targetToDelete = null;
  
    let statsElements = [];
    let targetRowElements = [];
  
    // Icon background colors for different stat types (retained from original)
    const iconColors = {
    "heroicons:users": "from-blue-500 to-indigo-600",
    "heroicons:user-circle": "from-green-500 to-emerald-600",
    "heroicons:user-plus": "from-purple-500 to-pink-600",
    "heroicons:user-minus": "from-red-500 to-pink-600",
    "heroicons:currency-dollar": "from-emerald-500 to-teal-600",
    "heroicons:shopping-cart": "from-purple-500 to-pink-600",
    "heroicons:chart-bar": "from-orange-500 to-red-600",
    "heroicons:trending-up": "from-green-500 to-emerald-600",
    "heroicons:fire": "from-red-500 to-pink-600",
    "heroicons:star": "from-yellow-500 to-orange-600",
    "heroicons:heart": "from-pink-500 to-rose-600",
    "heroicons:plus": "from-blue-500 to-indigo-600",
    "heroicons:document-text": "from-purple-500 to-pink-600",
    "heroicons:cog": "from-gray-500 to-slate-600",
    "heroicons:bell": "from-yellow-500 to-orange-600",
    "heroicons:envelope": "from-green-500 to-emerald-600",
    "heroicons:calendar": "from-red-500 to-pink-600",
    "heroicons:user-group": "from-indigo-500 to-purple-600",
    "heroicons:chart-pie": "from-teal-500 to-cyan-600",
  };

  
    // 🛑 UPDATED: Translated table columns (based on targetColumns)
    $: translatedTargetColumns = targetColumns.map(col => ({
        ...col,
        label: $_(`targets.${col.key}`) // Assuming your translation keys are now prefixed with 'targets'
    }));
  
    // 🛑 UPDATED: Translated object types (replaces translatedUserRoles)
    $: translatedObjectTypes = objectTypes.map(type => ({
        ...type,
        name: $_(`targets.${type.id}`),
    }));
  
    // 🛑 UPDATED: Translated object subtypes (replaces translatedUserStatuses)
    $: translatedObjectSubtypes = objectSubtypes.map(subtype => ({
        ...subtype,
        name: $_(`targets.${subtype.id}`),
    }));
  
    // 🛑 UPDATED: Translated user stats (based on targetStats)
    $: translatedTargetStats = targetStats.map(stat => ({
        ...stat,
        name: $_(`targets.${stat.name.toLowerCase().replace(' ', '_')}`),
        value: stat.value,
        change: stat.change,
        changeType: stat.changeType,
        icon: stat.icon,
    }));
    
    // NOTE: Animation logic remains the same
    onMount(() => {
      if (statsElements.length > 0) {
        staggerAnimate(statsElements, "fadeInUp", { delay: 0.1 });
      }
      if (targetRowElements.length > 0) {
        staggerAnimate(targetRowElements, "fadeInUp", { delay: 0.05 });
      }
    });
  
    // 🛑 UPDATED: Filter and sort targets
    $: {
      filteredTargets = dso // Use the dso data array
        .filter((target) => {
          const matchesSearch =
            target.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            target.object.toLowerCase().includes(searchTerm.toLowerCase()); // Searching name or object
          
          const matchesType = !selectedType || target.type === selectedType; // Replaces role
          const matchesSubtype = !selectedSubtype || target.subtype === selectedSubtype; // Replaces status
          const matchesKanbanStep = !selectedKanbanStep || target.kanban_step === selectedKanbanStep; // Replaces department
  
          return (
            matchesSearch && matchesType && matchesSubtype && matchesKanbanStep
          );
        })
        .sort((a, b) => {
          let aValue = a[sortBy];
          let bValue = b[sortBy];
  
          // NOTE: Date sorting logic is REMOVED as your data doesn't use these fields
          // if (sortBy === "lastActive" || sortBy === "joinDate") {
          //   aValue = new Date(aValue || 0);
          //   bValue = new Date(bValue || 0);
          // }
  
          if (sortDirection === "asc") {
            return aValue > bValue ? 1 : -1;
          } else {
            return aValue < bValue ? 1 : -1;
          }
        });
    }
  
    // NOTE: Sorting logic remains the same
    function handleSort(column) {
      if (sortBy === column) {
        sortDirection = sortDirection === "asc" ? "desc" : "asc";
      } else {
        sortBy = column;
        sortDirection = "asc";
      }
    }
  
    // 🛑 UPDATED: Get Type Info (replaces getRoleInfo)
    function getTypeInfo(typeId) {
      return translatedObjectTypes.find((type) => type.id === typeId);
    }
  
    // 🛑 UPDATED: Get Subtype Info (replaces getStatusInfo)
    function getSubtypeInfo(subtypeId) {
      return translatedObjectSubtypes.find((subtype) => subtype.id === subtypeId);
    }
    
    // NOTE: Date formatting functions are REMOVED/Simplified as your data doesn't use them
    // You can add formatting functions for 'size', 'integration', etc., if needed.
  
    function handleEditTarget(target) {
      selectedTarget = target;
      showTargetModal = true;
    }
  
    function handleDeleteTarget(target) {
      targetToDelete = target;
      showDeleteModal = true;
    }
  
    function handleDeleteConfirm() {
      if (targetToDelete) {
        // Handle delete logic here
        
        console.log("Delete target:", targetToDelete.object);
        targetToDelete = null;
      }
    }
  
    function handleDeleteCancel() {
      targetToDelete = null;
    }
  
    function clearFilters() {
      searchTerm = "";
      selectedType = "";
      selectedSubtype = "";
      selectedKanbanStep = "";
    }

    
  </script>
  
  <div class="space-y-8">
    <div
      class="relative overflow-hidden bg-gradient-to-r from-primary/5 via-secondary/5 to-accent/5 rounded-2xl p-6 border border-base-300/50"
      use:motionInView={{ animation: "fadeInDown" }}
    >
      <div class="absolute top-0 right-0 w-16 h-16 opacity-10">
        <Icon icon="heroicons:star" class="w-full h-full text-primary" />
      </div>
      <div class="absolute bottom-0 left-0 w-24 h-24 opacity-10">
        <Icon icon="heroicons:fire" class="w-full h-full text-secondary" />
      </div>
  
      <div class="relative flex items-center justify-between">
        <div>
          <h1 class="text-3xl font-bold text-primary">
            {$_("targets.title")}
          </h1>
          <p class="mt-2 text-sm text-base-content/70 max-w-md">
            {$_("targets.description")}
          </p>
        </div>
        <button
          class="btn btn-primary shadow-xl hover:shadow-2xl group relative overflow-hidden"
          on:click={() => (showAddTargetModal = true)}
          use:motionHover
        >
          <div
            class="absolute inset-0 bg-gradient-to-r from-primary to-secondary opacity-0 group-hover:opacity-100 transition-opacity duration-300"
          ></div>
          <div class="relative flex items-center">
            <div
              class="p-1.5 rounded-lg bg-primary-content/20 group-hover:bg-primary-content/30 transition-colors duration-300"
            >
              <Icon icon="heroicons:plus" class="w-5 h-5 mr-2" />
            </div>
            {$_("targets.add_target")}
          </div>
        </button>
      </div>
    </div>
  
    <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
      {#each translatedTargetStats as stat, index}
        <div
          bind:this={statsElements[index]}
          class="group relative overflow-hidden bg-gradient-to-br from-base-100 to-base-200/50 rounded-2xl shadow-md border border-base-300/50 p-5 hover:shadow-lg hover:scale-105 transition-all duration-300 backdrop-blur-sm"
          use:motionHover
        >
          <div
            class="absolute top-4 right-4 w-16 h-16 opacity-5 group-hover:opacity-10 transition-opacity duration-300"
          >
            <Icon icon={stat.icon} class="w-full h-full text-primary" />
          </div>
  
          <div
            class="absolute inset-0 bg-gradient-to-r from-primary/5 to-secondary/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-2xl"
          ></div>
  
          <div class="relative flex items-center">
            <div class="flex-shrink-0">
              <div
                class="w-14 h-14 bg-gradient-to-br {iconColors[stat.icon] || 'from-primary/20 to-secondary/20'} rounded-xl flex items-center justify-center shadow-md group-hover:shadow-lg transition-shadow duration-300"
              >
                <Icon
                  icon={stat.icon}
                  class="w-7 h-7 text-white group-hover:scale-110 transition-transform duration-300"
                />
              </div>
            </div>
            <div class="ml-4 flex-1">
              <p class="text-sm font-medium text-base-content/70 truncate">
                {stat.name}
              </p>
              <p
                class="text-3xl font-bold text-base-content group-hover:text-primary transition-colors duration-300"
              >
                {stat.value}
              </p>
            </div>
          </div>
          <div class="mt-4 relative">
            <span
              class="inline-flex items-baseline px-3 py-1 rounded-full text-sm font-medium shadow-sm {stat.changeType ===
              'positive'
                ? 'bg-success/20 text-success border border-success/30'
                : 'bg-error/20 text-error border border-error/30'}"
            >
              <Icon
                icon="heroicons:arrow-trending-up"
                class="-ml-1 mr-1 flex-shrink-0 self-center h-4 w-4 {stat.changeType ===
                'positive'
                  ? 'text-success'
                  : 'text-error'}"
              />
              {stat.change}
            </span>
            <span class="ml-2 text-sm text-base-content/60"
              >{$_("analytics.compared_to_previous")}</span
            >
          </div>
        </div>
      {/each}
    </div>
  
    <div
      class="relative overflow-hidden bg-gradient-to-br from-base-100 to-base-200/30 rounded-2xl shadow-md border border-base-300/50 p-6 backdrop-blur-sm"
      use:motionInView={{ animation: "fadeInUp" }}
    >
      <div class="absolute top-0 right-0 w-20 h-20 opacity-5">
        <Icon icon="heroicons:funnel" class="w-full h-full text-primary" />
      </div>
  
      <div
        class="relative flex flex-col lg:flex-row lg:items-center 
  lg:justify-between space-y-4 lg:space-y-0 lg:space-x-4"
      >
        <div class="flex-1">
          <div class="relative">
            <div
              class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"
            >
              <Icon
                icon="heroicons:magnifying-glass"
                class="h-5 w-5 text-base-content/40"
              />
            </div>
            <input
              type="text"
              bind:value={searchTerm}
              placeholder={$_("targets.search_targets")}
              class="block w-full pl-10 pr-3 py-2 border border-base-300 rounded-lg focus:outline-none 
  focus:ring-2 focus:ring-primary focus:border-primary text-sm bg-base-100 text-base-content placeholder-base-content/40"
            />
          </div>
        </div>
  
        <div class="flex flex-wrap gap-4">
          <select
            bind:value={selectedType}
            class="select select-bordered w-full sm:w-auto bg-base-100 border-base-300 focus:border-primary focus:ring-2 focus:ring-primary"
          >
            <option value="">{$_("targets.all_types")}</option>
            {#each translatedObjectTypes as type}
              <option value={type.id}>{type.name}</option>
            {/each}
          </select>
  
          <select
            bind:value={selectedSubtype}
            class="select select-bordered w-full sm:w-auto bg-base-100 border-base-300 focus:border-primary focus:ring-2 focus:ring-primary"
          >
            <option value="">{$_("targets.all_subtypes")}</option>
            {#each translatedObjectSubtypes as subtype}
              <option value={subtype.id}>{subtype.name}</option>
            {/each}
          </select>
  
          <select
            bind:value={selectedKanbanStep}
            class="select select-bordered w-full sm:w-auto bg-base-100 border-base-300 focus:border-primary focus:ring-2 focus:ring-primary"
          >
            <option value="">{$_("targets.all_steps")}</option>
            {#each kanbanSteps as step}
              <option value={step}>{$_(`targets.step_${step}`)}</option>
            {/each}
          </select>
  
          <button
            class="btn btn-ghost group hover:bg-base-200/80"
            on:click={clearFilters}
          >
            <div
              class="p-1 rounded bg-base-200 group-hover:bg-base-300 transition-colors duration-200"
            >
              <Icon icon="heroicons:x-mark" class="w-4 h-4 mr-2" />
            </div>
            {$_("common.clear_filters")}
          </button>
        </div>
      </div>
    </div>
  
    <div
      class="relative overflow-hidden bg-gradient-to-br from-base-100 to-base-200/30 rounded-2xl shadow-md border border-base-300/50 backdrop-blur-sm"
      use:motionInView={{ animation: "fadeInUp", delay: 0.2 }}
    >
      <div class="absolute top-0 right-0 w-24 h-24 opacity-5">
        <Icon icon="heroicons:table-cells" class="w-full h-full text-secondary" />
      </div>
  
      <div class="relative overflow-x-auto">
        <table class="min-w-full divide-y divide-base-300/50">
          <thead class="bg-base-200/50">
            <tr>
              {#each translatedTargetColumns as column}
                <th
                  scope="col"
                  class="px-6 py-4 text-left text-xs font-medium text-base-content/60 uppercase tracking-wider cursor-pointer hover:bg-base-300/50 transition-colors duration-200"
                  class:cursor-pointer={column.sortable}
                  on:click={() => column.sortable && handleSort(column.key)}
                >
                  <div class="flex items-center space-x-1">
                    <span>{column.label}</span>
                    {#if column.sortable && sortBy === column.key}
                      <Icon
                        icon={sortDirection === "asc"
                          ? "heroicons:chevron-up"
                          : "heroicons:chevron-down"}
                        class="h-4 w-4"
                      />
                    {/if}
                  </div>
                </th>
              {/each}
            </tr>
          </thead>
          <tbody class="bg-base-100 divide-y divide-base-300/50">
            {#each filteredTargets as target, index}
              <tr
                bind:this={targetRowElements[index]}
                class="hover:bg-base-200/50 transition-all duration-200 group"
              >
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <div class="flex-shrink-0 h-10 w-10 relative">
                      <img
                        src={generateUserAvatar(target.name)}
                        alt={target.name}
                        class="h-10 w-10 rounded-full shadow-sm group-hover:shadow-md transition-shadow duration-200"
                        on:error={(e) => {
                          const targetElement = e.target;
                          if (targetElement instanceof HTMLImageElement) {
                            targetElement.src = generateFallbackAvatar(target.name);
                          }
                        }}
                      />
                      </div>
                    <div class="ml-4">
                      <div
                        class="text-sm font-medium text-base-content group-hover:text-primary transition-colors duration-200"
                      >
                        {target.object}
                      </div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm text-base-content">{target.name}</div>
                </td>
                
                <td class="px-6 py-4 whitespace-nowrap">
                  {#if getTypeInfo(target.type)}
                    <span
                      class="px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full shadow-sm {getTypeInfo(
                        target.type,
                      ).color} border border-current/20"
                    >
                      {getTypeInfo(target.type).name}
                    </span>
                  {/if}
                </td>
              
                <td class="px-6 py-4 whitespace-nowrap">
                  {#if getSubtypeInfo(target.subtype)}
                    <span
                      class="px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full shadow-sm {getSubtypeInfo(
                        target.subtype,
                      ).color} border border-current/20"
                    >
                      {getSubtypeInfo(target.subtype).name}
                    </span>
                  {/if}
                </td>
                
                <td
                  class="px-6 py-4 whitespace-nowrap text-sm text-base-content/60"
                >
                  {target.size} {target.unit}
                </td>
                
                <td
                  class="px-6 py-4 whitespace-nowrap text-sm text-base-content/60"
                >
                  {target.best}
                </td>
                
                <td
                  class="px-6 py-4 whitespace-nowrap text-sm text-base-content/60"
                >
                  {target.integration} min
                </td>
                
                <td
                  class="px-6 py-4 whitespace-nowrap text-sm text-base-content/60"
                >
                  {$_(`targets.step_${target.kanban_step}`)}
                </td>
                
                <td
                  class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium"
                >
                  <div class="flex items-center space-x-3 justify-end">
                    <button
                      class="text-primary hover:text-primary-focus group"
                      on:click={() => handleEditTarget(target)}
                    >
                      <div
                        class="p-1.5 rounded-lg bg-primary/10 group-hover:bg-primary/20 transition-colors duration-200"
                      >
                        <Icon icon="heroicons:pencil-square" class="h-5 w-5" />
                      </div>
                    </button>
                    <button
                      class="text-error hover:text-error-focus group"
                      on:click={() => handleDeleteTarget(target)}
                    >
                      <div
                        class="p-1.5 rounded-lg bg-error/10 group-hover:bg-error/20 transition-colors duration-200"
                      >
                        <Icon icon="heroicons:trash" class="h-5 w-5" />
                      </div>
                    </button>
                  </div>
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    </div>
  </div>
  
