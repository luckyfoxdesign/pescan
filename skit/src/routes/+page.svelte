<script>
  // import { onMount } from "svelte";

  let file = null;
  let isDragging = false;
  let agents = [];
  let agentsNames = [];
  let noticeMessage = "";
  let total = 0;

  // agents = [
  //   {
  //     calculation_period: "04.2024",
  //     organization_charge: 559.82,
  //     organization_code: 34,
  //     organization_name: 'АО "ПСК"',
  //     recalculation: 0,
  //     services_list: [
  //       {
  //         service_charge: 559.82,
  //         service_name: "Электроснабжение",
  //       },
  //     ],
  //   },
  //   {
  //     calculation_period: "05.2024",
  //     organization_charge: 249.2,
  //     organization_code: 43,
  //     organization_name: 'НО "ФКР МКД СПб"',
  //     recalculation: 0,
  //     services_list: [
  //       {
  //         service_charge: 249.2,
  //         service_name: "Взнос на капитальный ремонт",
  //       },
  //     ],
  //   },
  //   {
  //     calculation_period: "04.2024",
  //     organization_charge: 174.8,
  //     organization_code: 90,
  //     organization_name: 'АО "НЭО"',
  //     recalculation: 0,
  //     services_list: [
  //       {
  //         service_charge: 174.8,
  //         service_name: "Обращение с ТКО",
  //       },
  //     ],
  //   },
  //   {
  //     calculation_period: "04.2024",
  //     organization_charge: 4210.03,
  //     organization_code: 631,
  //     organization_name: 'ООО "ЖКС № 2 Красногвардейского\nрайона"',
  //     recalculation: 0,
  //     services_list: [
  //       {
  //         service_charge: 612.41,
  //         service_name: "Водоотведение",
  //       },
  //       {
  //         service_charge: 1322.54,
  //         service_name: "Горячее водоснабжение",
  //       },
  //       {
  //         service_charge: 1019.54,
  //         service_name: "Отопление",
  //       },
  //       {
  //         service_charge: 537.14,
  //         service_name: "Холодное водоснабжение",
  //       },
  //       {
  //         service_charge: 37.45,
  //         service_name: "Очистка мусоропроводов",
  //       },
  //       {
  //         service_charge: 119.32,
  //         service_name: "Содержание и текущий ремонт лифтов",
  //       },
  //       {
  //         service_charge: 130.68,
  //         service_name: "Содержание общего имущества в МКД",
  //       },
  //       {
  //         service_charge: 138.44,
  //         service_name: "Текущий ремонт общего имущества в МКД",
  //       },
  //       {
  //         service_charge: 50.4,
  //         service_name: "Уборка и сан. очистка земельного участка",
  //       },
  //       {
  //         service_charge: 48.41,
  //         service_name: "Уборка лестничных клеток",
  //       },
  //       {
  //         service_charge: 85.46,
  //         service_name: "Управление многоквартирным домом",
  //       },
  //       {
  //         service_charge: 13.35,
  //         service_name: "Эксплуатация ОДПУ",
  //       },
  //       {
  //         service_charge: 24.89,
  //         service_name: "Горячее водоснабжение СОИ",
  //       },
  //       {
  //         service_charge: 7.18,
  //         service_name: "Отведение сточных вод ГВС СОИ",
  //       },
  //       {
  //         service_charge: 11.62,
  //         service_name: "Отведение сточных вод ХВС СОИ",
  //       },
  //       {
  //         service_charge: 11.62,
  //         service_name: "Холодное водоснабжение СОИ",
  //       },
  //       {
  //         service_charge: 7.77,
  //         service_name: "Электроэнергия ночь СОИ",
  //       },
  //       {
  //         service_charge: 31.81,
  //         service_name: "Электроэнергия СОИ",
  //       },
  //     ],
  //   },
  // ];

  function handleDragOver(event) {
    event.preventDefault();
    isDragging = true;
  }

  function handleDragLeave(event) {
    event.preventDefault();
    isDragging = false;
  }

  function handleDrop(event) {
    event.preventDefault();
    isDragging = false;
    const droppedFiles = event.dataTransfer.files;

    if (droppedFiles.length > 0 && droppedFiles[0].type === "application/pdf") {
      file = droppedFiles[0];
    } else {
      noticeMessage = "Прикреплять можно только PDF файлы.";
    }
  }

  function handleFileSelect(event) {
    const selectedFiles = event.target.files;
    if (
      selectedFiles.length > 0 &&
      selectedFiles[0].type === "application/pdf"
    ) {
      file = selectedFiles[0];
    } else {
      noticeMessage = "Выберите PDF файл.";
    }
  }

  async function handleSubmit(event) {
    event.preventDefault();

    if (!file) {
      noticeMessage = "Сначала выберите файл.";
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("api/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("File upload failed");
      }

      const responseData = await response.json();
      agents = responseData.data;
      // totalCharge = agents.reduce((accumulator, agent) => {
      //   const charge = agent.organization_charge;
      //   return accumulator + charge;
      // }, 0);

      total = calculateTotalCharge(agents);

      agentsNames = [];
      agentsNames = fillAgentsNames(agents);

      // console.log(`Total Charge: ${totalCharge.toFixed(2)}`);
      // console.log(agents);
    } catch (error) {
      // console.error(error);
      noticeMessage = "Не получилось прочитать файл.";
    }
  }

  // onMount(() => {
  //   agentsNames = fillAgentsNames(agents);
  //   // console.log(agentsNames);
  // });

  function fillAgentsNames(values) {
    let arr = [];
    values.forEach((e) => {
      let agentName = {
        name: e.organization_name,
        code: e.organization_code,
        details: false,
      };
      arr.push(agentName);
    });
    return arr;
  }

  function calculateTotalCharge() {
    return agents
      .reduce((accumulator, agent) => {
        const charge = agent.organization_charge;
        return accumulator + charge;
      }, 0)
      .toLocaleString("ru-RU", { style: "currency", currency: "RUB" });
  }

  function formatToRub(value) {
    return value.toLocaleString("ru-RU", {
      style: "currency",
      currency: "RUB",
    });
  }
</script>

<section class="w-full mb-40 mt-8">
  <div class="flex flex-col w-full md:w-8/12 sm:mx-auto px-4 gap-y-4">
    <h1 class="text-3xl">Рассчет платы за месяц</h1>
    <form on:submit|preventDefault={handleSubmit}>
      <div class="bg-white p-4 rounded-md">
        <div
          class:border-gray-300={!isDragging}
          class:bg-blue-100={isDragging}
          class:border-blue-500={isDragging}
          class="h-56 flex justify-center items-center border-2 border-dashed rounded cursor-pointer border-gray-300 hover:bg-blue-100 hover:border-blue-500"
          on:dragover={handleDragOver}
          on:dragleave={handleDragLeave}
          on:drop={handleDrop}
          on:click={() => document.getElementById("fileInput").click()}
        >
          {#if file}
            <p class="text-center">{file.name}</p>
          {:else}
            <p class="text-center">
              Перетащите PDF-файл в выделенную область <br /> или <br /> щелкните,
              чтобы выбрать его.
            </p>
          {/if}
        </div>
      </div>
      <input
        type="file"
        accept="application/pdf"
        on:change={(e) => handleFileSelect(e)}
        class="hidden"
        id="fileInput"
      />
      {#if noticeMessage != ""}
        <div
          class="bg-orange-100 border border-orange-500 p-4 rounded-md flex flex-col gap-y-4 mt-4"
        >
          <div>
            {noticeMessage}
          </div>
          <button
            class="py-2 px-4 w-fit rounded-md bg-blue-400 hover:bg-blue-700 text-white disabled:opacity-30 disabled:hover:bg-blue-400"
            on:click={() => {
              noticeMessage = "";
            }}>Понятно</button
          >
        </div>
      {/if}
      <div class="flex flex-col gap-y-2 sm:flex-row sm:gap-x-2 mt-8">
        <h2 class="text-2xl w-full">
          Сколько мне платить: <span class="font-bold">
            <!-- {formatToRub(calculateTotalCharge())} -->
            {total}
          </span>
        </h2>
        <div class="w-fit">
          <button
            type="submit"
            disabled={!file}
            class="py-2 px-4 rounded-md bg-green-400 hover:bg-green-700 text-white disabled:opacity-30 disabled:hover:bg-green-400"
            >Посчитать</button
          >
        </div>
      </div>
    </form>
    {#if total != 0}
      <div class="min-w-full">
        <div class="flex flex-row gap-x-2 px-2 mb-4">
          <div class="text-gray-500 w-full">Организация</div>
          <div class="text-gray-500 min-w-24 text-right">Период</div>
          <div class="text-gray-500 min-w-24 text-right">Сумма</div>
        </div>
        {#await agents}
          <p>Loading...</p>
        {:then agents}
          <div class="flex flex-col gap-y-4">
            {#each agents as agent}
              <div
                class="flex flex-col p-2 bg-white rounded-md hover:bg-blue-100 hover:cursor-pointer"
                on:click={() => {
                  let tmp = agentsNames;
                  let c = tmp.find((e) => e.code == agent.organization_code);
                  c.details = !c.details;
                  agentsNames = tmp;
                }}
              >
                <div class="flex gap-y-2 flex-col sm:flex-row gap-x-4">
                  <div class="w-full">
                    {agent.organization_name} ({agent.services_list.length})
                  </div>
                  <div class="flex flex-row ml-auto sm:ml-0 gap-x-2">
                    <div class="min-w-24 text-right">
                      {agent.calculation_period}
                    </div>
                    <div class="min-w-24 text-right font-semibold">
                      {formatToRub(agent.organization_charge)}
                    </div>
                  </div>
                </div>
                {#if agentsNames.find((e) => e.code == agent.organization_code)?.details}
                  <div class="flex flex-col gap-y-1 mt-2">
                    {#each agent.services_list as service, i}
                      <div
                        class="flex flex-row gap-x-4 hover:bg-blue-300 border-t py-2"
                      >
                        <div class="w-full flex flex-row gap-x-2 font-light">
                          <div class="w-4 text-gray-500 text-right">
                            {i + 1}
                          </div>
                          {service.service_name}
                        </div>
                        <div class="min-w-32 text-right">
                          {formatToRub(service.service_charge)}
                        </div>
                      </div>
                    {/each}
                  </div>
                {/if}
              </div>
            {/each}
          </div>
        {:catch error}
          <p>Error loading agents: {error.message}</p>
        {/await}
        <div class="flex flex-row gap-x-4 border-t pt-2 px-2">
          <div class="w-full text-right">Всего:</div>
          <div class="w-fit text-right font-semibold">
            <!-- {formatToRub(calculateTotalCharge())} -->
            {total}
          </div>
        </div>
      </div>
    {/if}
  </div>
</section>
