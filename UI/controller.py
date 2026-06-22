import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleBuildGraph(self, e):
        startY = self._view._ddYear1.value
        endY = self._view._ddYear2.value

        if not startY or not endY:
            self._view._txt_result.controls.append(
                ft.Text("Selezionare un anno di inzio ed uno di fine.", color="red")
            )
            self._view.update_page()
            return

        self._model.buildGraph(startY, endY)

        nodes, edges = self._model.getGraphDetails()
        self._view._txtGraphDetails.controls.append(
            ft.Text(f"Grafo correttamente creato.\nNumero di nodi: {len(nodes)}\nNumero di archi: {len(edges)}")
        )
        self._view.update_page()

    def handlePrintDetails(self, e):
        maxComp = self._model.getCompConn()
        for c in maxComp:
            self._view._txtGraphDetails.controls.append(
                ft.Text(f"{c[0]} - {c[1]}")
            )
        self._view.update_page()

    def handleCercaDreamChampionship(self, e):
        K = self._view._txtInSoglia.value
        M = self._view._txtInNumDiEdizioni.value
        try:
            intK = int(K)
            intM = int(M)
        except ValueError:
            self._view._txt_result.controls.append(
                ft.Text("Inserisci un numero intero per K ed M.", color="red")
            )
            self._view.update_page()
            return

        bestObj, bestI = self._model.handleCampionato(intK, intM)
        self._view._txt_result.controls.append(
            ft.Text(f"I campionati più 'INCREDIBILI' hanno un punteggio di {bestI} e sono:")
        )
        for c in bestObj:
            self._view._txt_result.controls.append(
                ft.Text(f"{c}")
            )
        self._view.update_page()

    def fillDdYears(self):
        years = self._model.getAllYears()
        for year in years:
            self._view._ddYear1.options.append(
                ft.dropdown.Option(int(year["year"]))
            )
            self._view._ddYear2.options.append(
                ft.dropdown.Option(int(year["year"]))
            )

