export const NWS_API_BASE = "https://api.weather.gov";
export const USER_AGENT = "weather-app/1.0";

export interface AlertFeature {
    properties: {
        event?: string;
        areaDesc?: string;
        severity?: string;
        status?: string;
        headline?: string;
        description?: string;
        instruction?: string;
    };
}

export interface ForecastPeriod {
    name?: string;
    temperature?: number;
    temperatureUnit?: string;
    windSpeed?: string;
    windDirection?: string;
    shortForecast?: string;
    detailedForecast?: string;
}

export interface AlertsResponse {
    features: AlertFeature[];
}

export interface PointsResponse {
    properties: {
        forecast?: string;
    };
}

export interface ForecastResponse {
    properties: {
        periods: ForecastPeriod[];
    };
}

/**
 * Make a request to the NWS API with proper error handling
 */
export async function makeNWSRequest<T>(url: string): Promise<T | null> {
    const headers = {
        "User-Agent": USER_AGENT,
        Accept: "application/geo+json",
    };

    try {
        const response = await fetch(url, { headers });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return (await response.json()) as T;
    } catch (error) {
        console.error("Error making NWS request:", error);
        return null;
    }
}

/**
 * Format an alert feature into a readable string
 */
export function formatAlert(feature: AlertFeature): string {
    const props = feature.properties;
    return [
        `Event: ${props.event || "Unknown"}`,
        `Area: ${props.areaDesc || "Unknown"}`,
        `Severity: ${props.severity || "Unknown"}`,
        `Status: ${props.status || "Unknown"}`,
        `Description: ${props.description || "No description available"}`,
        `Instructions: ${props.instruction || "No specific instructions provided"}`,
    ].join("\n");
}
