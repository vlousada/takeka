<script>
    import { onMount } from "svelte";
    import Icon from "@iconify/svelte";
    import { _ } from "svelte-i18n";
  
    // 1. 🛑 UPDATED: Only import static definitions from targets.js
    import {
        dso as staticTargetStats, // Renamed to avoid confusion with reactive stat
        objectTypes,
        objectSubtypes,
        kanbanSteps,
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
      
    // 2. NEW: Variables for data fetching and state
    const ASTRO_TARGETS_API_URL = "/api/targets/all";
    const ASTRO_TARGETS_API_IMG_URL = "/api/targets/image/";
    let dso = []; 
    let loading = true; // State for loading indicator
    let error = null; // State for error handling

    // 3. Filter and UI state variables (remain the same)
    let filteredTargets = []; 
    let searchTerm = "";
    let selectedType = "";
    let selectedSubtype = "";
    let selectedKanbanStep = "";
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
    "heroicons:cloud": "from-red-500 to-pink-600",
    "heroicons:star": "from-yellow-500 to-yellow-600",
    "heroicons:heart": "from-pink-500 to-rose-600",
    "heroicons:sparkles": "from-yellow-500 to-yellow-600",
    "heroicons:funnel": "from-yellow-500 to-red-600",
    "heroicons:table-cells": "from-green-500 to-lime-600",
    "hugeicons:galaxy": "from-cyan-500 to-blue-600",
    "famicons:telescope": "from-purple-500 to-purple-600",
    
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
  
    // 4. 🛑 NEW: Reactive target statistics calculation
    $: totalTargets = dso.length;
    $: nebulaeCount = dso.filter(target => target.type === 'nebula').length;
    $: galaxiesCount = dso.filter(target => target.type === 'galaxy').length;
    $: clustersCount = dso.filter(target => target.type === 'cluster').length;
    // $: processedCount = dso.filter(target => target.kanban_step === '3').length;

    // 5. 🛑 NEW: Reactive statistics object based on fetched data
    $: translatedTargetStats = [
        { name: $_("targets.total_targets"), value: totalTargets.toString(), change: '+0', changeType: 'positive', icon: 'famicons:telescope' },
        { name: $_("targets.nebulae"), value: nebulaeCount.toString(), change: '+0', changeType: 'positive', icon: 'heroicons:cloud' },
        { name: $_("targets.galaxies"), value: galaxiesCount.toString(), change: '+0', changeType: 'positive', icon: 'hugeicons:galaxy' },
        { name: $_("targets.clusters"), value: clustersCount.toString(), change: '+0', changeType: 'positive', icon: 'heroicons:sparkles' }
      ];
    
    // 6. 🛑 UPDATED: Data fetching logic in onMount
    onMount(async () => {
      try {
        const response = await fetch(ASTRO_TARGETS_API_URL);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        // Assume the API returns an array of objects matching the 'dso' structure
        dso = data["targets"]; 
        error = null;
      } catch (e) {
          console.error("Failed to fetch Astro Targets:", e);
          error = "Failed to load targets. Please check the API endpoint.";
          // Optionally, fall back to the static data if fetch fails
          dso = staticTargetStats;
      } finally {
        loading = false;
      }

      // Run animation logic after data load
      if (statsElements.length > 0) {
        staggerAnimate(statsElements, "fadeInUp", { delay: 0.1 });
      }
      if (targetRowElements.length > 0) {
        staggerAnimate(targetRowElements, "fadeInUp", { delay: 0.05 });
      }
    });

    // Filter and sort targets (Logic remains the same, but now reacts to 'dso')
    $: {
        filteredTargets = dso 
          .filter((target) => {
            const matchesSearch =
              target.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
              target.object.toLowerCase().includes(searchTerm.toLowerCase()); 
            
            const matchesType = !selectedType || target.type === selectedType; 
            const matchesSubtype = !selectedSubtype || target.subtype === selectedSubtype; 
            const matchesKanbanStep = !selectedKanbanStep || target.kanban_step === selectedKanbanStep; 

            return (
              matchesSearch && matchesType && matchesSubtype && matchesKanbanStep
            );
          })
          .sort((a, b) => {
            let aValue = a[sortBy];
            let bValue = b[sortBy];

            if (sortDirection === "asc") {
              return aValue > bValue ? 1 : -1;
            } else {
              return aValue < bValue ? 1 : -1;
            }
          });
      }
  
    // Helper functions (remain the same)
    function handleSort(column) {
      if (sortBy === column) {
        sortDirection = sortDirection === "asc" ? "desc" : "asc";
      } else {
        sortBy = column;
        sortDirection = "asc";
      }
    }

    function getTypeInfo(typeId) {
      return translatedObjectTypes.find((type) => type.id === typeId);
    }

    function getSubtypeInfo(subtypeId) {
      return translatedObjectSubtypes.find((subtype) => subtype.id === subtypeId);
    }

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
        // Logic to DELETE target via API call goes here
        console.log("Delete target:", targetToDelete.object);
        targetToDelete = null;
        showDeleteModal = false;
        // In a real app, you would refetch data or remove the target from the 'dso' array
      }
    }

    function handleDeleteCancel() {
      targetToDelete = null;
      showDeleteModal = false;
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
        <Icon icon="uil:focus-target" class="w-full h-full text-secondary" />
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
                        src={`${ASTRO_TARGETS_API_IMG_URL}${target.image_file}`}
                        alt={target.name}
                        class="h-10 w-10 rounded-full shadow-sm group-hover:shadow-md transition-shadow duration-200"
                        on:error={(e) => {
                          console.log("Image load error for", target.name);
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
                      class="px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full shadow-sm {getSubtypeInfo(target.subtype).color} border border-current/20"
                    >
                      {getSubtypeInfo(target.subtype).name}
                      
                    </span>
                  {/if}
                </td>
                
                <td
                  class="px-6 py-4 whitespace-nowrap text-sm text-base-content/60"
                >
                  {target.size}
                </td>
                
                <td
                  class="px-6 py-4 whitespace-nowrap text-sm text-base-content/60"
                >
                  {target.best}
                </td>
                
                <td
                  class="px-6 py-4 whitespace-nowrap text-sm text-base-content/60"
                >
                  {target.subs}s  <br>  {target.integration}hrs
                </td>
                
                <td
                  class="px-6 py-4 whitespace-nowrap text-sm text-base-content/60"
                >
                  {$_(`targets.step_${target.kanban_step}`)}
                </td>
                <td
                  class="px-6 py-4 whitespace-nowrap text-sm text-base-content/60"
                >
                  {target.gear}
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
  
