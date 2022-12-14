import { Writable, writable } from 'svelte/store';
import type { Metadata } from "../types";


interface TextSourcesConfig {
    main: string;
    enabledInDetails: Record<string, boolean>;
}


const DEFAULT_MAIN_TEXT_SOURCE = "fg"

export const textSourcesConfigStore: Writable<TextSourcesConfig> = writable({ main: DEFAULT_MAIN_TEXT_SOURCE, enabledInDetails: {} })

const LOCAL_STORAGE_KEY = 'textSourcesConfig';


function saveConfig(config: TextSourcesConfig) {
    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(config));
}


export function initTextSourcesConfig(metadata: Metadata) {
    const configDump = localStorage.getItem(LOCAL_STORAGE_KEY);
    let config: TextSourcesConfig;
    if (configDump === null)
        config = {
            main: DEFAULT_MAIN_TEXT_SOURCE,
            enabledInDetails: {},
        }
    else {
        config = JSON.parse(configDump);
    }

    for (const textSource of metadata.text_sources) {
        if (config.enabledInDetails[textSource] === undefined) {
            config.enabledInDetails[textSource] = true;
        }
    }
    textSourcesConfigStore.set(config);
    saveConfig(config);
}


export function setMainTextSource(newMainSource: string) {
    textSourcesConfigStore.update(config => {
        config.main = newMainSource;
        saveConfig(config);
        return config;
    })
}


export function toggleTextSourceEnabled(source: string) {
    textSourcesConfigStore.update(config => {
        config.enabledInDetails[source] = !config.enabledInDetails[source];
        saveConfig(config);
        return config;
    })
}


export function enableTextSource(source: string) {
    textSourcesConfigStore.update(config => {
        config.enabledInDetails[source] = true;
        saveConfig(config);
        return config;
    })
}
