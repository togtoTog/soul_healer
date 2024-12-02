class HttpUtils {
    static async fetchHttpData(url, options = {}) {
        try {
            const response = await fetch(url, options);
            if (!response.ok) {
                console.error('fetching data error! http status: ' + response.status);
                return null;
            }
            let resp = await response.json();
            if (resp && resp.code === 0 && resp.data) {
                return resp.data;
            }
            console.warn("fetching data warning: ", resp)
            return null;
        } catch (error) {
            console.error('fetching data error:', error);
            return null;
        }
    }

    /**
     * 提交post请求，数据格式为json
     * @param url 请求URL
     * @param data 数据
     */
    static async fetchHttpPost(url, data = {}) {
        return await this.fetchHttpData(url, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        })
    }
}

// 挂在到 window 上
window.HttpUtils = HttpUtils;
