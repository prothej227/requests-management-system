export const getRefValuesByCategory = async (category) => {
    const requestUrl = `${API.GET_REF_VALUE_BY_CAT}?category=${encodeURIComponent(category)}`;
    
    try {
        const response = await axios.get(requestUrl);
        return response.data || [];
    } catch (err) {
        console.error(`Error fetching reference values for category "${category}":`, err);
        throw new Error(err?.message || "Failed to fetch reference values from backend");
    }
};

