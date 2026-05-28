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

// Volta todos os estados geométricos para o "default"
export const resetGeometricStates = () => {
  rotateMsg.params.theta = 0;

  translateMsg.params.tx = 0;
  translateMsg.params.ty = 0;

  scaleMsg.params.sx = 0;
  scaleMsg.params.sy = 0;
}

//---------------
// Mensagens de transformações de intensidade
//--------------

export const intensityInvertMsg = $state({
  type: "intensity_invert",
  params: { applied: false }
});

export const intensityLogMsg = $state({
  type: "intensity_log",
  params: { applied: false }
});

export const intensityGammaMsg = $state({
  type: "intensity_gamma",
  params: { gamma: 0.0 }
});

export const intensityConstrastMsg = $state({
  type: "intensity_contrast",
  params: { entry_inverval: [0, 255], exit_interval: [0, 255] }
});

// Volta todos os estados das transformações de intensidade para o "default"
export const resetIntensityStates = () => {
  intensityInvertMsg.params.applied = false;
  intensityLogMsg.params.applied = false;

  intensityGammaMsg.params.gamma = 0.0;

  intensityConstrastMsg.params.entry_inverval = [0, 255];
  intensityConstrastMsg.params.exit_interval = [0, 255]
}
