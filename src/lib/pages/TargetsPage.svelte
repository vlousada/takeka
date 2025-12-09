<script>
  import { onMount } from "svelte";
  import { _ } from "svelte-i18n";
  import Icon from "@iconify/svelte";
  import {
      motionInView,
      staggerAnimate,
      motionHover,
    } from "../utils/motion.js";

  import { 
    getStatusColor,
    getStockColor,
    getStatusDisplayText
  } from "../data/products.js";

  import {
        dso as staticTargetStats, // Renamed to avoid confusion with reactive stat
        objectTypes,
        objectSubtypes,
        kanbanSteps,
        targetColumns,
        sortOptionsTargets
      } from "../data/targets.js";
    import { each } from "chart.js/helpers";
      
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
    let selectedSortBy = "name";
    let showAddTargetModal = false;
    let selectedTarget = null;
    let showTargetModal = false;
    let showDeleteModal = false;
    let targetToDelete = null;

    let statsElements = [];
    let targetRowElements = [];




  // Translated table columns (based on targetColumns)
  $: translatedTargetColumns = targetColumns.map(col => ({
      ...col,
      label: $_(`targets.${col.key}`) // Assuming your translation keys are now prefixed with 'targets'
  }));

  // Translated object types (replaces translatedUserRoles)
  $: translatedObjectTypes = objectTypes.map(type => ({
      ...type,
      name: $_(`targets.${type.id}`),
  }));

  // Translated object subtypes (replaces translatedUserStatuses)
  $: translatedObjectSubtypes = objectSubtypes.map(subtype => ({
      ...subtype,
      name: $_(`targets.${subtype.id}`),
  }));

  // NEW: Reactive target statistics calculation
  $: totalTargets = dso.length;
  $: nebulaeCount = dso.filter(target => target.type === 'nebula').length;
  $: galaxiesCount = dso.filter(target => target.type === 'galaxy').length;
  $: clustersCount = dso.filter(target => target.type === 'cluster').length;


  // Reactive statistics object based on fetched data
  $: translatedTargetStats = [
      { name: $_("targets.total_targets"), value: totalTargets.toString(), change: '+0', changeType: 'positive', icon: 'famicons:telescope' },
      { name: $_("targets.nebulae"), value: nebulaeCount.toString(), change: '+0', changeType: 'positive', icon: 'heroicons:cloud' },
      { name: $_("targets.galaxies"), value: galaxiesCount.toString(), change: '+0', changeType: 'positive', icon: 'hugeicons:galaxy' },
      { name: $_("targets.clusters"), value: clustersCount.toString(), change: '+0', changeType: 'positive', icon: 'heroicons:sparkles' }
    ];
    
 
  // Icon background colors for different stat types
  const iconColors = {
    'heroicons:plus': 'from-blue-500 to-indigo-600',
    'heroicons:magnifying-glass': 'from-gray-500 to-slate-600',
    'heroicons:document-text': 'from-teal-500 to-cyan-600',
    'heroicons:arrow-up': 'from-green-500 to-emerald-600',
    'heroicons:arrow-down': 'from-red-500 to-pink-600',
    'heroicons:pencil-square': 'from-blue-500 to-indigo-600',
    'heroicons:trash': 'from-red-500 to-pink-600',
    'heroicons:cube': 'from-orange-500 to-red-600',
    'heroicons:exclamation-triangle': 'from-yellow-500 to-orange-600',
    'heroicons:x-mark': 'from-gray-500 to-slate-600',
    "heroicons:cloud": "from-red-500 to-pink-600",
    "heroicons:star": "from-yellow-500 to-yellow-600",
    "heroicons:heart": "from-pink-500 to-rose-600",
    "heroicons:sparkles": "from-yellow-500 to-yellow-600",
    "heroicons:funnel": "from-yellow-500 to-red-600",
    "heroicons:table-cells": "from-green-500 to-lime-600",
    "hugeicons:galaxy": "from-cyan-500 to-blue-600",
    "famicons:telescope": "from-purple-500 to-purple-600",
  };

  
  // Data fetching logic in onMount
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


  // Computed filtered and sorted targets
  $: filteredTargets = dso.filter((target) => {
      //console.log("Filtering target:", target, "    with searchTerm:", searchTerm, "step:", selectedKanbanStep);
      const matchesSearch =
          target.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
          target.object.toLowerCase().includes(searchTerm.toLowerCase())||
          target.subtype.toLowerCase().includes(searchTerm.toLowerCase())||
          target.gear.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesType =
          !selectedType || target.type === selectedType;
      const matchesSubtype =
          !selectedSubtype || target.subtype === selectedSubtype;
      const matchesKanbanStep =
          !selectedKanbanStep || target.kanban_step === selectedKanbanStep;

      return matchesSearch && matchesType && matchesSubtype && matchesKanbanStep;
  });

  $: sortedTargets = [...filteredTargets].sort((a, b) => {
      let compareA, compareB;
      switch (selectedSortBy) {
        case "name":
          return a.name.localeCompare(b.name);
        case "name-desc":
          return b.name.localeCompare(a.name);
        case "subs":
          return Number(a.subs) - Number(b.subs);
        case "subs-desc":
          return Number(b.subs) - Number(a.subs);
        case "const":
          return a.constelation.localeCompare(b.constelation);
        case "const-desc":
          return b.constelation.localeCompare(a.constelation);
        default:
            return 0;
      }
  });



  // Functions Targets
  function openAddTargetModal() {
    showAddTargetModal = true;
  }
  function closeAddTargetModal() {
    showAddTargetModal = false;
    selectedTarget = null;
  }
  // function openDeleteConfirmation(target) {
  //   targetToDelete = target;
  //   showDeleteModal = true;
  // }



</script>


<div class="space-y-8">

  <!-- Page header with enhanced styling -->
  <div
    class="relative overflow-hidden bg-gradient-to-r from-primary/5 via-secondary/5 to-accent/5 rounded-2xl p-6 border border-base-300/50"
    use:motionInView={{ animation: "fadeInDown" }}
  >
    <!-- Background decorative elements -->
    <div class="absolute top-0 right-0 w-16 h-16 opacity-10">
      <Icon icon="uil:focus-target" class="w-full h-full text-primary" />
    </div>
    <div class="absolute bottom-0 left-0 w-24 h-24 opacity-10">
      <Icon icon="heroicons:shopping-cart" class="w-full h-full text-secondary" />
    </div>
    
    <div class="relative flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold text-primary">{$_("targets.title")}</h1>
        <p class="mt-2 text-sm text-base-content/70 max-w-md">
          {$_("targets.description")}
        </p>
      </div>
    </div>
  </div>

  <!-- Enhanced Filters and Search -->
  <div
          class="relative overflow-hidden bg-gradient-to-br from-base-100 to-base-200/30 rounded-2xl shadow-md border border-base-300/50 p-6 backdrop-blur-sm"
    use:motionInView={{ animation: "fadeInUp" }}
  >
    <!-- Background decoration -->
    <div class="absolute top-0 right-0 w-20 h-20 opacity-5">
      <Icon icon="heroicons:funnel" class="w-full h-full text-primary" />
    </div>
    
    <div class="relative grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <!-- Search -->
      <div class="lg:col-span-2">
        
        <label class="block text-sm font-medium text-base-content mb-2">{$_("targets.search_targets")}</label>
        <div class="join w-full">
          <div class="join-item flex-1">
            <input
              type="text"
              bind:value={searchTerm}
              placeholder={$_("targets.search_placeholder")}
              class="input input-bordered w-full bg-base-100 border-base-300 focus:border-primary focus:ring-2 focus:ring-primary"
            />
          </div>
          <button class="btn join-item hover:text-base-content">
            <div class="p-1 rounded bg-base-200 group-hover:bg-base-300 transition-colors duration-200">
              <Icon icon="heroicons:magnifying-glass" class="w-4 h-4" />
            </div>
          </button>
        </div>
      </div>

      <!-- Category Filter -->
      <div>
        <label class="block text-sm font-medium text-base-content mb-2"
          >{$_("targets.type")}
          <select
            bind:value={selectedType}
            class="select select-bordered w-full bg-base-100 border-base-300 focus:border-primary focus:ring-2 focus:ring-primary"
            >
            <option value="">{$_("targets.all_types")}</option>
            {#each translatedObjectTypes as type}
            <option value={type.id}>{type.name}</option>
            {/each}
          </select>
      </label>
      </div>

      <!-- Status Filter -->
      <div>
        <label class="block text-sm font-medium text-base-content mb-2"
          >{$_("targets.kanban")}
        </label>
        <select
          bind:value={selectedKanbanStep}
          class="select select-bordered w-full sm:w-auto bg-base-100 border-base-300 focus:border-primary focus:ring-2 focus:ring-primary"
          > 
          <option value="">{$_("targets.all_steps")}</option>
          {#each kanbanSteps as step}
          <option value={step.key}>{$_(`targets.step_${step.name}`)}</option>
          {/each}
        </select>
      </div>
    </div>

    <!-- Sort and Results -->
    <div
      class="relative flex flex-col sm:flex-row sm:items-center justify-between mt-6 pt-6 border-t border-base-300/50 gap-4"
    >
      <!-- Sort Options -->
      <div class="flex flex-wrap items-center gap-3">
        <span class="text-sm font-medium text-base-content/70">{$_("targets.sort_by")}</span>
        <div class="flex flex-wrap gap-2">
          {#each sortOptionsTargets as option}
            <button
              class="btn btn-sm {selectedSortBy === option.value ? 'btn-primary' : 'btn-ghost'} gap-2 group hover:shadow-md transition-all duration-200"
              on:click={() => selectedSortBy = option.value}
            >
              <div class="p-1 rounded {selectedSortBy === option.value ? 'bg-primary-content/10 group-hover:bg-primary-content/20' : 'bg-base-200 group-hover:bg-base-300'} transition-colors duration-200">
                {#if option.value.includes('desc')}
                  <Icon icon="heroicons:arrow-down" class="w-4 h-4" />
                {:else}
                  <Icon icon="heroicons:arrow-up" class="w-4 h-4" />
                {/if}
              </div>
              {option.label}
            </button>
          {/each}
        </div>
      </div>

      <!-- Results Count -->
      <div class="text-sm text-base-content/60 flex items-center gap-2">
        <div class="p-1 rounded bg-base-200">
          <Icon icon="heroicons:document-text" class="w-4 h-4" />
        </div>
        <span>{sortedTargets.length} {$_("targets.of")} {dso.length} {$_("targets.targets_found")}</span>
      </div>
    </div>
  </div>

  <!-- Enhanced TARGETS Grid -->
  <div
    class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
    use:motionInView={{ animation: "fadeInUp" }}
  >
    {#each sortedTargets as target, index}
      <div
        class="group relative overflow-hidden bg-gradient-to-br from-base-100 to-base-200/30 rounded-2xl shadow-md border border-base-300/50 hover:shadow-lg hover:scale-105 transition-all duration-300 backdrop-blur-sm"
        use:motionHover
      >
        <!-- Background decoration -->
        <div class="absolute top-0 right-0 w-16 h-16 opacity-5 group-hover:opacity-10 transition-opacity duration-300">
          <Icon icon="heroicons:cube" class="w-full h-full text-primary" />
        </div>
        
        <!-- Glow effect -->
        <div class="absolute inset-0 bg-gradient-to-r from-primary/5 to-secondary/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-2xl"></div>
        
        <!-- TARGET Image -->
        <figure class="relative h-48 bg-base-200">
          <img
            src={`${ASTRO_TARGETS_API_IMG_URL}${target.image_file}`}
            alt={target.name}
            class="w-full h-full object-cover"
            on:error={(event) => {
              const target = event.target;
              if (target instanceof HTMLImageElement) {
                target.src =
                  "https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=150&h=150&fit=crop";
              }
            }}  
          />
          <div class="absolute top-2 right-2">
                          <div class="badge {getStatusColor(target.status)} shadow-md">
              {getStatusDisplayText(target.status)}
            </div>
          </div>
        </figure>

        <!-- TARGET Info -->
        <div class="relative p-3">
          <div class="flex items-start justify-between mb-3">
            <h3 class="card-title text-sm line-clamp-2 group-hover:text-primary transition-colors duration-200">{target.name}</h3>
            <span class="text-xs">{target.constelation}</span>
            
          </div>

          <div
            class="flex items-center justify-between text-xs text-base-content/60 mb-3"
          >
            <span title="{target.notes}"> {target.object}</span>
            <span class="text-center">{target.type}</span>
            <span>{target.subtype}</span>
          </div>
          
          <hr>
          <p class="text-xs text-center mt-2 mb-2 line-clamp-2" style="color:#a570ff">
            {target.gear}
          </p>
          <hr>

          <div class="flex items-center justify-between mb-2">
            <span class="text-lg font-bold text-base-content group-hover:text-primary transition-colors duration-200"
              >{target.subs}s</span
            >
            <span class="text-sm font-medium {getStockColor(target.integration)}">
              {target.integration} {$_("targets.integration")}
            </span>
            <span class="text-sm font-medium">
              {target.best}
            </span>            
          </div>


        </div>
      </div>
    {/each}
  </div>

  <!-- Enhanced Empty State -->
  {#if sortedTargets.length === 0}
    <div
      class="relative overflow-hidden bg-gradient-to-br from-base-100 to-base-200/30 rounded-2xl shadow-md border border-base-300/50 backdrop-blur-sm"
      use:motionInView={{ animation: "fadeInUp" }}
    >
      <!-- Background decoration -->
      <div class="absolute top-0 right-0 w-24 h-24 opacity-5">
        <Icon icon="heroicons:cursor-arrow-ripple" class="w-full h-full text-primary" />
      </div>
      
      <div class="relative card-body text-center py-12">
        <Icon
          icon="heroicons:cursor-arrow-ripple"
          class="w-16 h-16 text-base-content/40 mx-auto mb-4"
        />
        <h3 class="text-lg font-medium text-base-content mb-2">
          {$_("targets.no_targets_found")}
        </h3>
        <p class="text-base-content/60 mb-6">
          {$_("users.try_adjusting_search")}
        </p>
        <button
          class="btn btn-primary shadow-md hover:text-primary-content group relative overflow-hidden"
          on:click={openAddTargetModal}
        >
          <div class="absolute inset-0 bg-gradient-to-r from-primary to-secondary opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          <div class="relative flex items-center">
            <div class="p-1 rounded bg-primary-content/10 group-hover:bg-primary-content/20 transition-colors duration-300">
              <Icon icon="heroicons:plus" class="w-4 h-4 mr-2" />
            </div>
            {$_("targets.add_first_target")}
          </div>
        </button>
      </div>
    </div>
  {/if}
</div>

<!-- Add/Edit TARGET Modal -->
{#if showAddTargetModal}
  <div class="modal modal-open">
    <div class="modal-box max-w-2xl">
      <div class="flex items-center justify-between mb-4">
        <h3 class="font-bold text-lg">
          {selectedTarget ? $_("targets.edit_target") : $_("targets.add_new_target")}
        </h3>
        <button
          class="btn btn-sm btn-circle btn-ghost hover:text-base-content"
          on:click={closeAddTargetModal}
        >
          <Icon icon="heroicons:x-mark" class="w-4 h-4" />
        </button>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="form-control">
          <label class="label">
            <span class="label-text">{$_("targets.name")}</span>
            <input
              type="text"
              class="input input-bordered"
              placeholder={$_("targets.target_name_placeholder")}
              />
          </label>
        </div>

        <div class="form-control">
          <label class="label">
            <span class="label-text">{$_("targets.type")}</span>
            <select class="select select-bordered">
              <option value="">{$_("targets.select_type")}</option>
              <option value="Nebulae">{$_("targets.nebulae")}</option>
              <option value="Galaxies">{$_("targets.galaxies")}</option>
              <option value="Clusters">{$_("targets.clusters")}</option>
            </select>
          </label>
        </div>

        <div class="form-control">
          <label class="label">
            <span class="label-text">{$_("targets.subs")}</span>
            <input
              type="number"
              step="1"
              class="input input-bordered"
              placeholder={$_("targets.subs_placeholder")}
              />
          </label>
        </div>

        <div class="form-control">
          <label class="label">
            <span class="label-text">{$_("targets.integration")}</span>
            <input type="number" class="input input-bordered" placeholder={$_("targes.integration_placeholder")} />
          </label>
        </div>

        <div class="form-control">
          <label class="label">
            <span class="label-text">{$_("targets.object")}</span>
            <input
              type="text"
              class="input input-bordered"
              placeholder={$_("targets.object_placeholder")}
            />
          </label>
        </div>

        <div class="form-control">
          <label class="label">
            <span class="label-text">{$_("target.status")}</span>
            <select class="select select-bordered">
              <option value="0">{$_("targets.todo")}</option>
              <option value="1">{$_("targes.planning")}</option>
              <option value="2">{$_("targes.starting")}</option>
              <option value="3">{$_("targes.imaging")}</option>
              <option value="4">{$_("targes.processing")}</option>
              <option value="5">{$_("targets.reviewing")}</option>
              <option value="9">{$_("targets.completed")}</option>
            </select>
          </label>
        </div>

        <div class="form-control md:col-span-2">
          <label class="label">
            <span class="label-text">{$_("targets.gear")}</span>
            <textarea
              rows="3"
              class="textarea textarea-bordered"
              placeholder={$_("targets.gear_placeholder")}
              ></textarea>
          </label>
        </div>

        <div class="form-control md:col-span-2">
          <label class="label">
            <span class="label-text">{$_("targets.image_url")}</span>
            <input
              type="url"
              class="input input-bordered"
              placeholder={$_("targets.image_url_placeholder")}
            />
          </label>
        </div>
      </div>

      <div class="modal-action">
        <button class="btn btn-outline hover:text-base-content" on:click={closeAddTargetModal}>
          {$_("settings.cancel")}
        </button>
        <button
                      class="btn btn-primary shadow-md hover:text-primary-content"
          on:click={closeAddTargetModal}
        >
          {selectedTarget ? $_("targets.update_target") : $_("targets.add_target")}
        </button>
      </div>
    </div>
  </div>
{/if}


