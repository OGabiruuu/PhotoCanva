<script>
    import logoImg from '../assets/camera-retro-org.png';
    import geometricTransformIcon from '../assets/recursos-org.png';
    import intensityTransformIcon from '../assets/funcao-quadrada-org.png';
    import effectTransformIcon from '../assets/brilhos-org.png';

    import NavBarButton from '$lib/components/NavBarButton.svelte';
    import {toolSetManager} from '$lib/globalStates/uiStates.svelte'
</script>


<div id="navBar-container">
    <!-- <h3>PhotoCanva</h3> -->
    <img id="navBar-logo" src={logoImg} alt="Logo" title="PhotoCanva">

    <div id="navBar-options">
        <!-- Transformações geométricas -->
        <NavBarButton
            toolSetIconSrc={geometricTransformIcon}
            toolSetName="Transformações geométricas"
            isActive={toolSetManager.activeTool === 'geometric'}
            onClickHandler={() => {toolSetManager.activeTool = 'geometric'}}
        />

        <!-- Transformações de intensidade -->
        <NavBarButton
            toolSetIconSrc={intensityTransformIcon}
            toolSetName="Transformações de intensidade"
            isActive={toolSetManager.activeTool === 'intensity'}
            onClickHandler={() => {toolSetManager.activeTool = 'intensity'}}
        />

        <!-- Efeitos -->
        <NavBarButton
            toolSetIconSrc={effectTransformIcon}
            toolSetName="Efeitos"
            isActive={toolSetManager.activeTool === 'effect'}
            onClickHandler={() => {toolSetManager.activeTool = 'effect'}}
        />
    </div>
</div>

<style>
    #navBar-container {
        height: 100%;
        width: 2%;
        padding: 4% 2% 0% 2%;
        z-index: 2;

        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        gap: 5%;

        background-color: var(--clr-outer-box);
        box-shadow: 8px 6px 8px rgba(10, 10, 10, 0.4);
    }

    #navBar-logo {
        padding-top: 5%;
        padding-bottom: 55%;

        border-bottom: solid 3px var(--clr-inner-box);

        max-width: 100%;
        max-height: 100%;
        object-fit: cover;  /*Mantém a proporção da imagem*/
    }

    #navBar-options {
        height: 100%;
        display: felx;
        flex-direction: column;
        justify-content: space-around;
    }
</style>
