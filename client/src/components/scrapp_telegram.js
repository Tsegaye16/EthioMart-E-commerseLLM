import React, { useState } from "react";
import { Table, Input, Button, message, Space, Upload } from "antd";
import { UploadOutlined } from "@ant-design/icons";
import {
  fetchTelegramData,
  normalizeTelegramData,
  getNormalizedData,
} from "../service/api_service";
import axios from "axios";
import { downloadFile } from "../utils/file_util";

const TelegramFetcher = () => {
  const [channel, setChannel] = useState("");
  const [file, setFile] = useState(null);
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleFetchData = async () => {
    if (!channel) {
      message.warning("Please enter a Telegram channel.");
      return;
    }
    try {
      setLoading(true);
      await fetchTelegramData(channel);
      message.success("Data fetched successfully!");
    } catch (error) {
      message.error(error?.response?.data?.error || "Error fetching data.");
    } finally {
      setLoading(false);
    }
  };

  const handleNormalizeData = async () => {
    if (!file) {
      message.warning("Please upload a JSON or CSV file to normalize.");
      return;
    }

    try {
      setLoading(true);
      const formData = new FormData();
      formData.append("file", file);

      const response = await axios.post("/api/normalize", formData, {
        responseType: "blob", // Ensure the response is treated as a file
      });

      // Create a download link for the processed file
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "processed_data.json"); // Set default download name
      document.body.appendChild(link);
      link.click(); // Trigger download
      document.body.removeChild(link); // Clean up

      message.success("Data normalized successfully!");
    } catch (error) {
      console.error("Error normalizing data:", error);
      message.error(
        error?.response?.data?.error ||
          "Error normalizing data. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleDisplayData = async () => {
    if (!channel) {
      message.warning("Please enter a Telegram channel.");
      return;
    }
    try {
      const result = await getNormalizedData(`data/processed/${channel}.json`);
      setData(result);
    } catch (error) {
      message.error(error?.response?.data?.error || "Error loading data.");
    }
  };

  const handleFileChange = (info) => {
    console.log(info.file);
    const file = info.file?.originFileObj; // Safely access the file
    if (!file) {
      message.error("Failed to retrieve the file. Please try again.");
      return;
    }
    if (!["application/json", "text/csv"].includes(file.type)) {
      message.error("Only JSON or CSV files are supported.");
      return;
    }
    setFile(file);
    message.success(`${file.name} selected for normalization.`);
  };

  const handleDownload = (type) => {
    if (data.length === 0) {
      message.warning("No data to download.");
      return;
    }
    const fileName = `${channel}_data.${type}`;
    const fileData =
      type === "json"
        ? JSON.stringify(data, null, 2)
        : type === "csv"
        ? data
            .map((row) =>
              Object.values(row)
                .map((value) => `"${value}"`)
                .join(",")
            )
            .join("\n")
        : data.map((row) => Object.values(row).join(" ")).join("\n");
    const fileType =
      type === "json"
        ? "application/json"
        : type === "csv"
        ? "text/csv"
        : "text/plain";
    downloadFile(fileData, fileName, fileType);
    message.success(`Data saved as ${fileName}`);
  };

  const columns = [
    { title: "ID", dataIndex: "id", key: "id" },
    { title: "Text", dataIndex: "cleaned_text", key: "cleaned_text" },
  ];

  return (
    <div style={{ padding: 20 }}>
      <Space direction="vertical" style={{ width: "100%" }}>
        <Input
          placeholder="Enter Telegram Channel"
          value={channel}
          onChange={(e) => setChannel(e.target.value)}
        />
        <Space>
          <Button type="primary" onClick={handleFetchData} loading={loading}>
            Fetch Data
          </Button>
          <Upload
            // beforeUpload={() => false} // Prevent auto-upload by Ant Design
            onChange={handleFileChange}
            accept=".json,.csv"
            showUploadList={false}
          >
            <Button icon={<UploadOutlined />}>Upload File</Button>
          </Upload>
          <Button onClick={handleNormalizeData} loading={loading}>
            Normalize Data
          </Button>
          <Button onClick={handleDisplayData}>Display Table</Button>
        </Space>
      </Space>
      <Table
        dataSource={data}
        columns={columns}
        rowKey="id"
        style={{ marginTop: 20 }}
        pagination={{ pageSize: 10 }}
      />
      {data.length > 0 && (
        <Space style={{ marginTop: 20 }}>
          <Button onClick={() => handleDownload("csv")}>Download as CSV</Button>
          <Button onClick={() => handleDownload("json")}>
            Download as JSON
          </Button>
          <Button onClick={() => handleDownload("txt")}>Download as TXT</Button>
        </Space>
      )}
    </div>
  );
};

export default TelegramFetcher;
