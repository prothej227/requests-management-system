import axios from "axios";
import { toast } from "vue3-toastify";

export const getRefValuesByCategory = async (category) => {
  const requestUrl = `${API.GET_REF_VALUE_BY_CAT}?category=${encodeURIComponent(
    category,
  )}`;

  try {
    const response = await axios.get(requestUrl);
    return response.data || [];
  } catch (err) {
    console.error(
      `Error fetching reference values for category "${category}":`,
      err,
    );
    throw new Error(
      err?.message || "Failed to fetch reference values from backend",
    );
  }
};

export const toProperCase = (str) => {
  if (!str) return "";
  return str.replace(/\w\S*/g, function (txt) {
    return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
  });
};

export const getItemByUrl = async (url) => {
  try {
    const response = await axios.get(url);
    if (response.status === 200) {
      return response.data;
    } else {
      toast.error("An unknown error occured. Status code: ", response.status);
    }
  } catch (error) {
    toast.error("An error occured: ", error.message);
  }
};
