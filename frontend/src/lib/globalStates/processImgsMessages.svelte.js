//---------------
// Mensagens de transformações geométricas
//--------------

const rotateMsg = $state({
  type: "rotate",
  params: { theta: 0 }
});

const translateMsg = $state({
  type: "translate",
  params: { tx: 0, ty: 0 }
});

const scaleMsg = $state({
  type: "scale",
  params: { sx: 1, sy: 1 }
});


//---------------
// Mensagens de transformações de intensidade
//--------------

const intensityInvertMsg = $state({
  type: "intensity_invert",
  params: {}
});

const intensityLogMsg = $state({
  type: "intensity_log",
  params: {}
});

const intensityGammaMsg = $state({
  type: "intensity_gamma",
  params: { gamma: 0.0 }
});

const intensityConstrastMsg = $state({
  type: "intensity_contrast",
  params: { entry_inverval: [], exit_interval: [] }
});
