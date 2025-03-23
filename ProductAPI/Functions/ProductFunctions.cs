using System;
using System.IO;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Extensions.Http;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using ProductAPI.Data;
using ProductAPI.Models;

namespace ProductAPI.Functions
{
    public class ProductFunctions
    {
        private readonly ProductDbContext _dbContext;

        public ProductFunctions(ProductDbContext dbContext)
        {
            _dbContext = dbContext;
        }

        [FunctionName("GetProducts")]
        public async Task<IActionResult> GetProducts(
            [HttpTrigger(AuthorizationLevel.Function, "get", Route = "products")] HttpRequest req,
            ILogger log)
        {
            log.LogInformation("Getting all products");

            try
            {
                var products = await _dbContext.GetAllProductsAsync();
                return new OkObjectResult(products);
            }
            catch (Exception ex)
            {
                log.LogError(ex, "Error getting products");
                return new StatusCodeResult(StatusCodes.Status500InternalServerError);
            }
        }

        [FunctionName("GetProductById")]
        public async Task<IActionResult> GetProductById(
            [HttpTrigger(AuthorizationLevel.Function, "get", Route = "products/{id}")] HttpRequest req,
            ILogger log,
            int id)
        {
            log.LogInformation($"Getting product with ID: {id}");

            try
            {
                var product = await _dbContext.GetProductByIdAsync(id);
                if (product == null)
                {
                    return new NotFoundResult();
                }

                return new OkObjectResult(product);
            }
            catch (Exception ex)
            {
                log.LogError(ex, $"Error getting product with ID: {id}");
                return new StatusCodeResult(StatusCodes.Status500InternalServerError);
            }
        }

        [FunctionName("CreateProduct")]
        public async Task<IActionResult> CreateProduct(
            [HttpTrigger(AuthorizationLevel.Function, "post", Route = "products")] HttpRequest req,
            ILogger log)
        {
            log.LogInformation("Creating a new product");

            try
            {
                string requestBody = await new StreamReader(req.Body).ReadToEndAsync();
                var product = JsonConvert.DeserializeObject<Product>(requestBody);

                if (product == null)
                {
                    return new BadRequestResult();
                }

                if (string.IsNullOrEmpty(product.Name) || product.Price <= 0)
                {
                    return new BadRequestObjectResult(
                        "Product name is required and price must be greater than zero.");
                }

                int newProductId = await _dbContext.CreateProductAsync(product);
                product.Id = newProductId;

                return new CreatedResult($"api/products/{newProductId}", product);
            }
            catch (Exception ex)
            {
                log.LogError(ex, "Error creating product");
                return new StatusCodeResult(StatusCodes.Status500InternalServerError);
            }
        }

        [FunctionName("UpdateProduct")]
        public async Task<IActionResult> UpdateProduct(
            [HttpTrigger(AuthorizationLevel.Function, "put", Route = "products/{id}")] HttpRequest req,
            ILogger log,
            int id)
        {
            log.LogInformation($"Updating product with ID: {id}");

            try
            {
                var existingProduct = await _dbContext.GetProductByIdAsync(id);
                if (existingProduct == null)
                {
                    return new NotFoundResult();
                }

                string requestBody = await new StreamReader(req.Body).ReadToEndAsync();
                var updatedProduct = JsonConvert.DeserializeObject<Product>(requestBody);

                if (updatedProduct == null)
                {
                    return new BadRequestResult();
                }

                updatedProduct.Id = id;  // Ensure ID matches route parameter

                if (string.IsNullOrEmpty(updatedProduct.Name) || updatedProduct.Price <= 0)
                {
                    return new BadRequestObjectResult(
                        "Product name is required and price must be greater than zero.");
                }

                bool result = await _dbContext.UpdateProductAsync(updatedProduct);
                
                if (result)
                {
                    return new OkObjectResult(updatedProduct);
                }
                else
                {
                    log.LogWarning($"Product with ID {id} was not updated. No rows affected.");
                    return new StatusCodeResult(StatusCodes.Status500InternalServerError);
                }
            }
            catch (Exception ex)
            {
                log.LogError(ex, $"Error updating product with ID: {id}");
                return new StatusCodeResult(StatusCodes.Status500InternalServerError);
            }
        }

        [FunctionName("DeleteProduct")]
        public async Task<IActionResult> DeleteProduct(
            [HttpTrigger(AuthorizationLevel.Function, "delete", Route = "products/{id}")] HttpRequest req,
            ILogger log,
            int id)
        {
            log.LogInformation($"Deleting product with ID: {id}");

            try
            {
                var existingProduct = await _dbContext.GetProductByIdAsync(id);
                if (existingProduct == null)
                {
                    return new NotFoundResult();
                }

                bool result = await _dbContext.DeleteProductAsync(id);
                
                if (result)
                {
                    return new NoContentResult();
                }
                else
                {
                    log.LogWarning($"Product with ID {id} was not deleted. No rows affected.");
                    return new StatusCodeResult(StatusCodes.Status500InternalServerError);
                }
            }
            catch (Exception ex)
            {
                log.LogError(ex, $"Error deleting product with ID: {id}");
                return new StatusCodeResult(StatusCodes.Status500InternalServerError);
            }
        }
    }
} 