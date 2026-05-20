//---------------
// Mensagens de transformações geométricas
//--------------

export const rotateMsg = $state({
  type: "rotate",
  params: { theta: 0 }
});

export const translateMsg = $state({
  type: "translate",
  params: { tx: 0, ty: 0 }
});

export const scaleMsg = $state({
  type: "scale",
  params: { sx: 1, sy: 1 }
});


//---------------
// Mensagens de transformações de intensidade
//--------------

export const intensityInvertMsg = $state({
  type: "intensity_invert",
  params: {  }
});

export const intensityLogMsg = $state({
  type: "intensity_log",
  params: { }
});

export const intensityGammaMsg = $state({
  type: "intensity_gamma",
  params: { gamma: 0.0 }
});

export const intensityConstrastMsg = $state({
  type: "intensity_contrast",
  params: { entry_inverval: [], exit_interval: [] }
});
