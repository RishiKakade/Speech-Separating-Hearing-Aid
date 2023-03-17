import re
import numpy as np
from datetime import datetime

log_file = "rpi.txt"
start_pattern = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - chunk_http_tx_to_IS_start")
end_pattern = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - chunk_http_tx_to_IS_end")

chunk_http_tx_to_IS_start = []
chunk_http_tx_to_IS_end = []

with open(log_file, "r") as f:
    for line in f:
        start_match = start_pattern.search(line)
        end_match = end_pattern.search(line)
        if start_match:
            chunk_http_tx_to_IS_start.append(datetime.strptime(start_match.group(1), "%Y-%m-%d %H:%M:%S,%f"))
        elif end_match:
            chunk_http_tx_to_IS_end.append(datetime.strptime(end_match.group(1), "%Y-%m-%d %H:%M:%S,%f"))


#####################


log_file = "async_server_log.txt"

chunk_http_rx_from_rpi_end_pattern = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - chunk_http_rx_from_rpi_end")
chunk_http_rx_from_rpi_start_pattern = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - chunk_http_rx_from_rpi_start")
chunk_convert_bytes_end_pattern = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - chunk_convert_bytes_end")
chunk_convert_bytes_start_pattern = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - chunk_convert_bytes_start")
chunk_write_end_pattern = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - chunk_write_end")
chunk_write_start_pattern = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - chunk_write_start")
inference_new_chunk_pattern = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - inference_new_chunk_pattern")
inference_cos_end_pattern = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - inference_cos_end_pattern")
inference_convtas_pattern = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - inference_convtas_pattern")
inference_write_to_color_buffer_pattern = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - inference_write_to_color_buffer_pattern")
inference_removing_chunk_file_pattern = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - inference_removing_chunk_file_pattern")
inference_end_pattern = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - inference_end_pattern")
chunk_http_tx_to_WS_start = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - chunk_http_tx_to_WS_start")
chunk_http_tx_to_WS_end = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - chunk_http_tx_to_WS_end")


chunk_http_rx_from_rpi_end = []
chunk_http_rx_from_rpi_start = []
chunk_convert_bytes_end = []
chunk_convert_bytes_start = []
chunk_write_end = []
chunk_write_start = [] 
inference_new_chunk = []
inference_cos_end = []
inference_convtas = []
inference_write_to_color_buffer = []
inference_removing_chunk_file = [] 
inference_end = []
chunk_http_tx_to_WS_start = []
chunk_http_tx_to_WS_end =  []

with open(log_file, "r") as f:
    for line in f:
        match1 = chunk_http_rx_from_rpi_end_pattern.search(line)
        match2 = chunk_http_rx_from_rpi_start_pattern.search(line)
        match3 = chunk_convert_bytes_end_pattern.search(line)
        match4 = chunk_convert_bytes_start_pattern.search(line)
        match5 = chunk_write_end_pattern.search(line)
        match6 = chunk_write_start_pattern.search(line)
        match7 = inference_new_chunk_pattern.search(line)
        match8 = inference_cos_end_pattern.search(line)
        match9 = inference_convtas_pattern.search(line)
        match10 = inference_write_to_color_buffer_pattern.search(line)
        match11 = inference_removing_chunk_file_pattern.search(line)
        match12 = inference_end_pattern.search(line)
        match13 = chunk_http_tx_to_WS_start
        match14 = chunk_http_tx_to_WS_end

        if match1:
            chunk_http_rx_from_rpi_end.append(datetime.strptime(match1.group(1), "%Y-%m-%d %H:%M:%S,%f"))
        elif match2:
            chunk_http_rx_from_rpi_start.append(datetime.strptime(match2.group(1), "%Y-%m-%d %H:%M:%S,%f"))
        elif match3:
            chunk_convert_bytes_end.append(datetime.strptime(match3.group(1), "%Y-%m-%d %H:%M:%S,%f"))
        elif match4:
            chunk_convert_bytes_start.append(datetime.strptime(match4.group(1), "%Y-%m-%d %H:%M:%S,%f"))
        elif match5:
            chunk_write_end.append(datetime.strptime(match5.group(1), "%Y-%m-%d %H:%M:%S,%f"))
        elif match6:
            chunk_write_start.append(datetime.strptime(match6.group(1), "%Y-%m-%d %H:%M:%S,%f"))
        elif match7:
            inference_new_chunk.append(datetime.strptime(match7.group(1), "%Y-%m-%d %H:%M:%S,%f"))
        elif match8:
            inference_cos_end.append(datetime.strptime(match8.group(1), "%Y-%m-%d %H:%M:%S,%f"))
        elif match9:
            inference_convtas.append(datetime.strptime(match9.group(1), "%Y-%m-%d %H:%M:%S,%f"))
        elif match10:
            inference_write_to_color_buffer.append(datetime.strptime(match10.group(1), "%Y-%m-%d %H:%M:%S,%f"))
        elif match11:
            inference_removing_chunk_file.append(datetime.strptime(match11.group(1), "%Y-%m-%d %H:%M:%S,%f"))
        elif match12:
            inference_end.append(datetime.strptime(match12.group(1), "%Y-%m-%d %H:%M:%S,%f"))
        elif match13:
            chunk_http_tx_to_WS_start.append(datetime.strptime(match13.group(1), "%Y-%m-%d %H:%M:%S,%f"))
        elif match14:
            chunk_http_tx_to_WS_end.append(datetime.strptime(match14.group(1), "%Y-%m-%d %H:%M:%S,%f"))

# total http transfer time  0.5*((chunk_http_tx_to_IS_end - chunk_http_tx_to_IS_start) - (chunk_http_rx_from_rpi_end - chunk_http_rx_from_rpi_start)) 






################





log_file = "web_server_log.txt"

chunk_http_tx_to_client_end_pattern = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - chunk_http_tx_to_client_end_pattern =")
chunk_http_tx_to_client_start_pattern = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - chunk_http_tx_to_client_start_pattern =")
chunk_http_rx_from_IS_end_pattern = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - chunk_http_rx_from_IS_end_pattern =")
chunk_http_rx_from_IS_start_pattern = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - chunk_http_rx_from_IS_start_pattern =")

chunk_http_tx_to_client_end = []
chunk_http_tx_to_client_start = []
chunk_http_rx_from_IS_end = []
chunk_http_rx_from_IS_start = []

with open(log_file, "r") as f:
    for line in f:
        match1 = chunk_http_tx_to_client_end_pattern.search(line)
        match2 = chunk_http_tx_to_client_start_pattern.search(line)
        match3 = chunk_http_rx_from_IS_end_pattern.search(line)
        match4 = chunk_http_rx_from_IS_start_pattern.search(line)

        if match1:
            chunk_http_tx_to_client_end.append(datetime.strptime(match1.group(1), "%Y-%m-%d %H:%M:%S,%f"))
        if match2:
            chunk_http_tx_to_client_start.append(datetime.strptime(match2.group(1), "%Y-%m-%d %H:%M:%S,%f"))
        if match3:
            chunk_http_rx_from_IS_end.append(datetime.strptime(match3.group(1), "%Y-%m-%d %H:%M:%S,%f"))
        if match4:
            chunk_http_rx_from_IS_start.append(datetime.strptime(match4.group(1), "%Y-%m-%d %H:%M:%S,%f"))



################
#calculation
################

rpi_tx_difference = [(end - start).total_seconds() for start, end in zip(chunk_http_tx_to_IS_start, chunk_http_tx_to_IS_end)]
rpi_tx_average_difference = sum(rpi_tx_difference) / len(rpi_tx_difference)

print(f"Average difference between chunk_http_tx_to_IS_end and chunk_http_tx_to_IS_start: {rpi_tx_average_difference:.3f} milliseconds")
print(f"Median difference between chunk_http_tx_to_IS_end and chunk_http_tx_to_IS_start: {np.median(rpi_tx_difference):.3f} milliseconds")
print(f"Max difference between chunk_http_tx_to_IS_end and chunk_http_tx_to_IS_start: {np.max(rpi_tx_difference):.3f} milliseconds")



IS_rx_difference = [(end - start).total_seconds() for start, end in zip(chunk_http_rx_from_rpi_start, chunk_http_rx_from_rpi_end)]
print(chunk_http_rx_from_rpi_start)
#IS_rx_average_difference = sum(IS_rx_difference) / len(IS_rx_difference)
#
#print(f"Average difference between chunk_http_rx_from_rpi_end and chunk_http_rx_from_rpi_start, {IS_rx_average_difference:.3f} milliseconds")
#print(f"Median difference between chunk_http_rx_from_rpi_end and chunk_http_rx_from_rpi_start: {np.median(IS_rx_difference):.3f} milliseconds")
#print(f"Max difference between chunk_http_rx_from_rpi_end and chunk_http_rx_from_rpi_end: {np.max(IS_rx_difference):.3f} milliseconds")
#
#
#rpi_IS_http_transfer_time = 0.5*((chunk_http_tx_to_IS_end - chunk_http_tx_to_IS_start) - (chunk_http_rx_from_rpi_end - chunk_http_rx_from_rpi_start)) 
#
#IS_WS_http_transfer_time = 0.5*((chunk_http_tx_to_WS_end - chunk_http_tx_to_WS_start)-(chunk_http_rx_from_IS_end - chunk_http_rx_from_IS_start))

#WS_WC_http_transfer_time = 0.5*((chunk_http_tx_to_client_end - chunk_http_tx_to_client_start)-(chunk_http_rx_UI_from_WS_end - chunk_http_rx_UI_from_WS_start))

#inference time

################
#plots
################