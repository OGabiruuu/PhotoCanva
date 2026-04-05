// Closure que gera o estado da sessão de ferramentas ativas na toolbar como um singleton
function CreateToolSetManager() {
  let activeTool = $state('geometric');

  return {
    get activeTool() { return activeTool },
    set activeTool(v) { activeTool = v }
  };
}
export const toolSetManager = CreateToolSetManager()
